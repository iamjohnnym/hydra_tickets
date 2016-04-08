from app import db
import datetime

class Callbacks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    phone = db.Column(db.Integer)
    ddi = db.Column(db.Integer, index = True)
    ticket = db.Column(db.Integer, index = True)
    platform = db.Column(db.String(64), index = True)
    created = db.Column(db.DateTime, index = True, default=datetime.datetime.utcnow())
    details = db.relationship('CallbackDetails', backref='comments', lazy='dynamic')
    viewing = db.relationship('ActiveTickets', backref='active', lazy='dynamic')

    def __repr__(self):
        return '<User %r' % (self.name)

class CallbackDetails(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    updated = db.Column(db.DateTime)
    details = db.Column(db.String(64))
    private = db.Column(db.String(64))
    status = db.Column(db.String(64), index = True, default='new')
    callbacks_id = db.Column(db.Integer, db.ForeignKey('callbacks.id'))
    user_name = db.Column(db.String(128), db.ForeignKey('user.displayName'))
    #user = db.relationship('User', backref='active', lazy='dynamic')

    def __repr__(self):
        return '<User %r' % (self.id)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sso = db.Column(db.String(96), unique=True)
    displayName = db.Column(db.String(72))
    email = db.Column(db.String(128))
    manager = db.Column(db.String(200))
    responses = db.relationship('CallbackDetails', backref='responses', lazy='dynamic')
    active = db.relationship('ActiveTickets', backref='viewing_tickets', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r' % (self.sso)

class ActiveTickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('callbacks.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<User %r' % (self.id)

db.create_all()
