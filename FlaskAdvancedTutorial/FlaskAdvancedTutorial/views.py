"""
Routes and views for the flask application.
"""
import os
from config import app, db
from datetime import datetime
#request allows us to use if request.method == "POST" because it is bound to a view
#flash allows us to use session messages. However we will need to set a secret key.
from flask import render_template, url_for, Flask, request, redirect, flash
#import our form class
from forms import BookmarkForm
#import the models
from models import Bookmark, User

#Fake Login
def logged_in_user():
    return models.User.query.filter_by(username="admin").first()

#/home view
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Bookmark Saver',
        year=datetime.now().year,
        new_bookmarks = Bookmark.newest(5))

#/add view
@app.route("/add", methods=["GET", "POST"])
def add():
    #POST
    #we are using the form we created in forms.py
    form = BookmarkForm()
    if form.validate_on_submit(): #checks http form or validation errors
        #otherwise lets add the data
        url = form.url.data
        description = form.description.data
        #store the bookmak in the database
        bm = Bookmark(user=logged_in_user(), url=url, description=description)
        db.session.add(bm)
        db.session.commit()
        #let the user know all is well
        flash("Stored '{}'".format(description))
        return redirect(url_for("home"))
    
    #GET
    #if not validate on submit, show the new form.
    return render_template("add.html",  
                           title='Bookmark Saver',
                           year=datetime.now().year,
                           form=form)

#/user/username
@app.route("/user/<username>")
def user(username):
    #find the first username matching or return 404
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user.html", user=user)



#some route playing a did
def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
            # links is now a list of url, endpoint tuples