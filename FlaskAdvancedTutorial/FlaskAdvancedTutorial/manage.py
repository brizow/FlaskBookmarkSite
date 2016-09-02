from FlaskAdvancedTutorial import app, db, User
from flask.ext import Manager, prompt_bool

manager = Manager(app)

#create the database commands
@manager.command
def initdb():
    db.create_all()
    #add one toplevel user
    db.session.add(User(username="admin", email="admin@admin.com"))
    db.session.commit()
    print "Initialized the database"

@manager.command
def dropdb():
    if prompt_bool(
        "Are you sure you want to lose all your data?"):
        db.drop_all()
        print "Dropped the database swuccessfully."

if __name__ == "__main__":
    manager.run