import os
from config import *
#models need to be loaded so that migrate can access them
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

#app creation class to initializes all of our require components
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)

    #load dependancies after we initialize their parents above.
    #import blueprints and register
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix="/")

    from .bookmarks import bookmarks as bkm_blueprint
    app.register_blueprint(bkm_blueprint, url_prefix="/bookmarks")

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app

app = create_app(os.getenv("FLASK_ENV") or "dev")

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

#app creation class to initializes all of our require components
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)

    #load dependancies after we initialize their parents above.
    #import blueprints and register
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix="/")

    from .bookmarks import bookmarks as bkm_blueprint
    app.register_blueprint(bkm_blueprint, url_prefix="/bookmarks")

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app

#run the server using local host
if __name__ == "__main__":
    manager.run()
