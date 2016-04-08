import os

basedir = os.path.abspath(os.path.dirname(__file__))
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'hydra.db') + '?check_same_thread=False'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# form validation
CSRF_ENABLED = True
SECRET_KEY = 'Shibby do boo opp'
