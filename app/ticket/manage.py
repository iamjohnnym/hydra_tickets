#-*- coding: utf-8 -*-

from flask import render_template, flash, redirect, session, url_for, request, Markup
from app.internalapi.api import GlobalApi
from app.sendmail.mail import SendMail
from flask import Markup
import datetime
import requests


class Ticket():
    def __init__(self, user=None):
        self.api = GlobalApi()
        self.user = user

    def list(self, endpoint):
        return self.api.get_all(endpoint)

    def add(self, form):
        timestamp = str(datetime.datetime.utcnow())
        ticket_details = {'ddi':form.ddi.data,
                'ticket':form.ticket.data,
                'name':form.name.data,
                'phone':form.phone.data,
                'platform':form.platform.data,
                'details':[
                    {'details': form.details.data,
                     'updated':timestamp,
                     'user_name':self.user,
                     'private':None
                     }
                ]
            }
        try:
            id = self.api.post('callbacks', ticket_details)['id']
#            sendmail = SendMail(
#                    recipient='your.name@mail.com',
#                    status='New',
#                    id=id,
#                    **ticket_details
#                    ).run()
            msg = Markup("New callback has been created for {0}.  To view, go \
                    here: <a href=\"/callbacks/{1}\">View</a>".format(
                        ticket_details['name'],
                        id
                        )
                    )
            return msg
        except requests.exceptions.RequestException,e:
            print e

    def update(self, ticket, form):
        updated = str(datetime.datetime.utcnow())
        dictionary = {'details':
                    {'add':
                        {'details': form.details.data,
                          'status': form.status.data,
                          'private': form.private.data,
                          'user_name': self.user,
                          'updated': updated,
                          }
                     }
                }
        put = self.api.put('callbacks', ticket, dictionary)
        # redundant.  fixthe self.api.put() to return the correct data
        ticket_details = self.api.get('callbacks', ticket)
        details = {}
        details['details'] = [{
                    'details': form.details.data,
                    'status': form.status.data,
                    'private': form.private.data,
                    'user_name': self.user,
                    'updated': updated,
                    }]
        li = []
        for key in put:
            for x in ['viewing', 'created']:
                if key == x:
                    li.append(key)
        for key in li:
            del put[key]

#        sendmail = SendMail(recipient='your.name@email.com',
#                            ddi=ticket_details['ddi'],
#                            name=ticket_details['name'],
#                            phone=ticket_details['phone'],
#                            ticket=ticket_details['ticket'],
#                            platform=ticket_details['platform'],
#                            details=details['details'],
#                            id=ticket,
#                            user_name=self.user,
#                            status=details['details'][0]['status']
#                            )
#        message = sendmail.run()
        return ticket_details


class Template():
    def __init__(self, globals):
        self.g = globals

    def list(self, tickets):
        return render_template("sb-admin/list.js.html",
            title='Ticket List',
            callbacks=tickets,
            g=self.g
            )

    def ticket(self, ticket_details, form):
        title = 'Ticket for {0}'.format(ticket_details['name'])
        return render_template("sb-admin/details.js.html",
            title=title,
            callbacks=ticket_details,
            form=form,
            g=self.g
            )

    def add(self, form):
        return render_template("sb-admin/add.html",
            title='Ticket Form',
            form=form,
            g=self.g
            )

