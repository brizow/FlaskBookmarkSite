#system imports
from datetime import datetime
from sqlalchemy import desc
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
#class imports
from config import app, db

#represents a table
class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    #add relation to user table
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    #static query method, used in the views page
    @staticmethod
    def newest(num):
        return Bookmark.query.order_by(desc(Bookmark.date)).limit(num)

    #enable clear printing and reading of values
    def __repr__(self):
        return "<Bookmark '{}': '{}'>".format(self.description, self.url)

#usermixin handles the authentication methods
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    #add relation to bookmarks, uses the idkey in bookmarks, backref hold user info
    bookmarks = db.relationship("Bookmark", backref="user", lazy="dynamic")
    password_hash = db.Column(db.String)

    #from werkzeug.security used here.

    #set the property as a string but only read it as a hash
    @property
    def password(self):
        raise AttributeError("password: write-only field")

    #generate a hash, set it in the password variable
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    #hash the entered password and compare to the hash above
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    #get the login name from the model instead of passing to the view
    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return "<User '{}'>".format(self.username)