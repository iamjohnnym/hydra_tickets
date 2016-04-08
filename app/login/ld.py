from app import db
from app.models import User
from flask import session
#import ldap


class Ld():
    def __init__(self, user):
        self.user = user
        self.ldap_server = "ldaps://auth.ldap.service"
        self.ldap_port = "636"
        self.ldap_url = "{0}:{1}".format(
                self.ldap_server,
                self.ldap_port
                )
        self.dn = "cn={0},ou=users,o=organization".format(
                self.user
                )

    def ldapFetch(self, passwd):
        try:
            user = self.checkUser()
#            if self.user and passwd:
#                connection = ldap.initialize(
#                        "{0}".format(
#                            self.ldap_url
#                            )
#                        )
#                connection.simple_bind_s(
#                        self.dn,
#                        passwd)
#                user = connection.search_s(
#                        self.dn,
#                        ldap.SCOPE_SUBTREE,
#                        '(cn={0})'.format(self.user),
#                        ['cn', 'mail', 'name', 'displayName', 'manager']
#                        )
#                return user
            return user
#        except ldap.LDAPError, e:
#            print e
        except Exception, e:
            print e

    def checkUser(self):
        check = User.query.filter_by(sso=self.user).first()
        return check


    def addUser(self, user):
        d = {}
        cn, info = user[0]
        for k, v in info.iteritems():
            if 'cn' in k:
                k = 'sso'
            if 'mail' in k:
                k = 'email'
            d[k] = v[0]
        try:
            insert = User(**d)
            db.session.add(insert)
            db.session.commit()
        except:
            db.session.rollback()
            return False

    def getLogin(self):
        user = User.query.filter_by(sso=self.user).first()
        session['remember_me'] = False
        if session['remember_me']:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        return user

