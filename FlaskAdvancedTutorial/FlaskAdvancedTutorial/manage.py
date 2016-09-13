from os import environ
from config import app, db
from models import Bookmark, User
from flask_script import Manager, prompt_bool
from views import *

manager = Manager(app)

#unfortunetly I can not get these to run using the manage script. I'm missing something...

#create the database commands
@manager.command
def initdb():
    db.create_all()
    #add one toplevel user
    db.session.add(User(username="admin", email="admin@admin.com"))
    db.session.commit()
    print "Initialized the database."

@manager.command
def dropdb():
    if prompt_bool(
        "Are you sure you want to lose all your data?"):
            db.drop_all()
            print "Dropped the database successfully."

