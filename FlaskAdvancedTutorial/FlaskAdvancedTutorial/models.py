from datetime import datetime
from sqlalchemy import desc
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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    #add relation to bookmarks, uses the idkey in bookmarks, backref hold user info
    bookmarks = db.relationship("Bookmark", backref="user", lazy="dynamic")

    def __repr__(self):
        return "<User %r" % self.username