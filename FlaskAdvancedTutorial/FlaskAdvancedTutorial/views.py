"""
Routes and views for the flask application.
"""
#system imports
import os
from config import app, db, login_manager
from datetime import datetime
#request allows us to use if request.method == "POST" because it is bound to a view
#flash allows us to use session messages. However we will need to set a secret key.
from flask import render_template, url_for, Flask, request, redirect, flash, abort
#login stuff
from flask_login import login_required, login_user, logout_user, current_user

#class imports
#import our form class
from forms import BookmarkForm, LoginForm, SignupForm
#import the models
from models import Bookmark, User, Tag

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
        tags = form.tags.data
        #store the bookmak in the database
        bm = Bookmark(user=current_user, url=url, description=description, tags=tags)
        db.session.add(bm)
        db.session.commit()
        #let the user know all is well
        flash("Stored '{}'".format(description))
        return redirect(url_for("home"))
    
    #GET
    #if not validate on submit, show the new form.
    return render_template("add.html", form=form, 
                           title="Bookmark Saver",
                           year=datetime.now().year)

#/edit/bookmarkid 
@app.route("/edit/<int:bookmark_id>", methods=["GET", "POST"])
@login_required
def edit_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    #if the bookmark is not owned by the user, forbidden
    if current_user != bookmark.user:
        abort(403)
    #pass the bookmark as an arg, WTF function here
    form = BookmarkForm(obj=bookmark)
    if form.validate_on_submit():
        #fill the form with data from the database
        form.populate_obj(bookmark)
        #if all checks out, submit the data
        db.session.commit()
        #tell the user all is well
        flash("Stored: '{}'".format(bookmark.description))
        return redirect(url_for("user", username=current_user.username))
    return render_template("bookmark_form.html", form=form, title="Edit Bookmark", 
                           year=datetime.now().year)

#/delete/bookmarkid 
@app.route("/delete/<int:bookmark_id>", methods=["GET", "POST"])
@login_required
def delete_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    #if the bookmark is not owned by the user, forbidden
    if current_user != bookmark.user:
        abort(403)
    if request.method == "POST":
        db.session.delete(bookmark)
        db.session.commit()
        flash("Bookmark '{}' has been deleted.".format(bookmark.url))
        return redirect(url_for("user", username=current_user.username))
    else:
        flash("Please confirm bookmark deletion.")
    return render_template("confirm_delete.html", bookmark=bookmark, nolinks=True)


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

#/tag/name
@app.route("/tag/<name>")
def tag(name):
    #try to retrieve a tag by name, if none 404, otherwise return template
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template("tag.html", tag=tag, title = "Tags Listing",
                           year=datetime.now().year)

#decorate a function like this to run before any template is rendered
@app.context_processor
def inject_tags():
    #tags list is now globally available for each template
    return dict(all_tags = Tag.all)



#some route playing a did
#def has_no_empty_params(rule):
#    defaults = rule.defaults if rule.defaults is not None else ()
#    arguments = rule.arguments if rule.arguments is not None else ()
#    return len(defaults) >= len(arguments)


#@app.route("/site-map")
#def site_map():
#    links = []
#    for rule in app.url_map.iter_rules():
#        # Filter out rules we can't navigate to in a browser
#        # and rules that require parameters
#        if "GET" in rule.methods and has_no_empty_params(rule):
#            url = url_for(rule.endpoint, **(rule.defaults or {}))
#            links.append((url, rule.endpoint))
#            # links is now a list of url, endpoint tuples