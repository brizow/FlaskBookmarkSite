"""
Routes and views for the authentication methods.
"""
#system imports
from flask import render_template
#class imports
from . import main
#import our form class
from . import login_manager
#db imports
from . import User, Bookmark, Tag

#give the redirector from login a place to go to. In this case
#it needs the userid from the User model.
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

#/home view
@main.route('/')
@main.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        "index.html",
        title='Bookmark Saver',
        year=datetime.now().year,
        new_bookmarks = Bookmark.newest(5))

#decorate a function like this to run before any template is rendered
#in the blueprint method use .app_ to register this globally on the app.
@main.app_context_processor
def inject_tags():
    #tags list is now globally available for each template
    return dict(all_tags = Tag.all)
