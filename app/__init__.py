from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.socketio import SocketIO
from flask.ext.restless import APIManager
from flask.ext.babel import Babel, lazy_gettext
from flask.ext.login import LoginManager
from momentjs import momentjs


app = Flask(__name__)
app.debug = True
app.config.from_object('config')
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = lazy_gettext('Please log in to access this page.')
db = SQLAlchemy(app)
api = APIManager(app, flask_sqlalchemy_db=db)
babel = Babel(app)
socketio = SocketIO(app)
app.jinja_env.globals['momentjs'] = momentjs

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/hydra.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Hydra Startup')

from app import views, models, api_views, socket_views
