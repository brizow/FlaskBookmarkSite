"""
The flask application package.
"""
#import our base path for postgres
#basedir = os.path.abspath(os.path.dirname(__file__))
from os import environ
from config import app
from models import Bookmark, User
from views import *
from manage import initdb, dropdb
"""
This script runs the WMS application using a development server.
"""


if __name__ == '__main__':
    initdb
    
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
