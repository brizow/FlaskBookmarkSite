"""
Routes and views for the flask application.
"""
#system imports
import os
from config import app, db, login_manager
from datetime import datetime
#request allows us to use if request.method == "POST" because it is bound to a view
#flash allows us to use session messages. However we will need to set a secret key.
from flask import render_template, url_for, Flask, request, redirect, flash
#login stuff
from flask_login import login_required, login_user, logout_user, current_user

#class imports
#import our form class
from forms import BookmarkForm, LoginForm, SignupForm
#import the models
from models import Bookmark, User

#give the redirector from login a place to go to. In this case
#it needs the userid from the User model.
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

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
#add the decorator to require login
@login_required
def add():
    #POST
    #we are using the form we created in forms.py
    form = BookmarkForm()
    if form.validate_on_submit(): #checks http form or validation errors
        #otherwise lets add the data
        url = form.url.data
        description = form.description.data
        #store the bookmak in the database
        bm = Bookmark(user=current_user, url=url, description=description)
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
@login_required
def user(username):
    #find the first username matching or return 404
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user.html", user=user, 
                           title = "Saved Bookmarks", 
                           year=datetime.now().year)


#/login
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #get the username from the model
        user = User.get_by_username(form.username.data)
        #if there is a user and the password is correct
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Loggin in successfully as {}.".format(user.username))
            #this redirects us to the page we were trying to get to or the user route
            return redirect(request.args.get("next") or url_for("user", username=user.username))
        #if username or password is incorrect
        flash("Incorrect Username or Password. Please try again.")
    return render_template("login.html", form=form, title = "Login", 
                           year=datetime.now().year)

#/logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

#/signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        #get the user signup info from form
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        #try adding that to database
        db.session.add(user)
        db.session.commit()
        flash("Welcome {}! Please login.".format(user.username))
        return redirect(url_for("login"))
    return render_template("signup.html", form=form, title = "Sign Up", 
                           year=datetime.now().year)  

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