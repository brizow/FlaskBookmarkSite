from os import environ
from config import app, db
#models need to be loaded so that migrate can access them
from models import User, Bookmark, Tag
from flask_script import Manager, prompt_bool, Server
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
#add specifics to the manager.py for autostart
manager.add_command("runserver", Server(host="localhost", port="8080"))
#you must run scripting commands outside of the python interactive window.

#migrate constructor, migreate commands preface with db
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)

#create the database commands
@manager.command
def initdb():
    db.create_all()
    #manually add toplevel users
    db.session.add(User(username="admin", email="admin@example.com", password="test"))
    db.session.add(User(username="user", email="user@example.com", password="test"))
    db.session.commit()
    print "Initialized the database."

@manager.command
def dropdb():
    if prompt_bool(
        "Are you sure you want to lose all your data?"):
            db.drop_all()
            print "Dropped the database successfully."

#load the models and the views otherwise, the server has
#no idea you have any routes.
import models
import views

#run the server using local host
if __name__ == "__main__":
    manager.run()
