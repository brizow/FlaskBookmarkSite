from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment

app = Flask(__name__)
app.config['DEBUG'] = True

#initialize the database object
db = SQLAlchemy(app)

#setup the secret session key
app.secret_key = '\x1f\x9b\xfb\x83"n\x16\xf5y\xc5{\xf6i\xd1\xb0\x81h_p\xd6e\xa0\xea'
#database config
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://user:user123@localhost/fat"

#configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

#for displaying nice js timestamps
moment = Moment(app)