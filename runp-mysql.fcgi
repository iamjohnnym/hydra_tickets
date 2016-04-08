#!flask/bin/python

# use mysql
import os
os.environ['DATABASE_URL'] = 'mysql://hydra:Thr33HeadedDragon@10.179.195.72/hydra'

from flup.server.fcgi import WSGIServer
from app import app

if __name__ == '__main__':
    WSGIServer(app).run()
