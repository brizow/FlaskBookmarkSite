from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True

#initialize the database object
db = SQLAlchemy(app)

#setup the secret session key
app.secret_key = '\x1f\x9b\xfb\x83"n\x16\xf5y\xc5{\xf6i\xd1\xb0\x81h_p\xd6e\xa0\xea'
#database config
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://user:user123@localhost/fat"
