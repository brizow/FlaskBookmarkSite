"""
The flask application package.
"""
from os import environ
#from config import app, db
#models need to be loaded so that migrate can access them
from models import User
from flask_script import Manager, prompt_bool, Server
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
    


##load the models and the views otherwise, the server has
##no idea you have any routes.
#import models

##run the server using local host
#if __name__ == "__main__":
#    manager.run()