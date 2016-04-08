from flask.ext.login import login_user, logout_user, current_user, login_required
from internalapi.api import GlobalApi
from sendmail.mail import SendMail
from ticket.manage import Ticket, Template
from ticket.forms import CallbackSubmit, CallbackUpdate
from login.forms import LoginForm
from login.ld import Ld
from models import Callbacks, User
from flask import render_template, flash, redirect, session, url_for, request, Markup, g, jsonify
from app import app, db, babel, lm
import datetime
import requests


#######
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        ld = Ld(form.sso.data)
        valid = ld.ldapFetch(form.password.data)
        if valid:
            check = ld.checkUser()
            if not check:
                ld.addUser(valid)
            user = ld.getLogin()
            login_user(user)
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash("Invalid SSO or Password")
    return render_template(
            "sb-admin/login.html",
            form=form
            )

@app.route('/', methods=['GET', 'POST'])
@app.route('/callbacks', methods=['GET', 'POST'])
@login_required
def index():
    ticket = Ticket()
    template = Template(g.user)
    tickets = ticket.list('callbacks')
    return template.list(tickets)

@app.route('/callbacks/add', methods = ['GET', 'POST'])
@login_required
def add():
    ticket = Ticket(user=g.user.displayName)
    template = Template(g.user)
    form = CallbackSubmit()
    if form.validate_on_submit():
        msg = ticket.add(
                form
                )
        flash(msg)
        return redirect(url_for('index'))
    return template.add(form)

@app.route('/callbacks/<ticket_id>', methods=['GET', 'POST', 'PUT'])
@login_required
def ticket(ticket_id):
    template = Template(g.user)
    form = CallbackUpdate()
    iapi = GlobalApi()
    ticket_details = iapi.get(
            'callbacks',
            ticket_id
            )
    if form.validate_on_submit():
        ticket = Ticket(
                user=g.user.displayName
                )
        ticket_details = ticket.update(
                ticket_id,
                form
                )
        form = CallbackUpdate()
        return template.ticket(ticket_details, form)
    return template.ticket(ticket_details, form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def internal_error(error):
    return render_template('errors/404.html'), 404
