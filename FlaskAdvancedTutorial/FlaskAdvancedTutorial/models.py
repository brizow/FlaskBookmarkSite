#these are our models for the Bookmark and User tables.
from datetime import datetime
from FlaskAdvancedTutorial.views import db

#Bookmark table
class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))

    def __repr__(self):
        return "<Bookmark '{}': '{}'>".format(self.description, self.url)

#User table    
class User(db.model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    #printable representation of the object
    def __repr__(self):
        return "<User %r" % self.username

