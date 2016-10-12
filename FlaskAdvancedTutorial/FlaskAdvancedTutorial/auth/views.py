"""
Routes and views for the authentication methods.
"""
#system imports
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user
#class imports
from . import auth #our auth blueprint
from . import db
#import our form class
from . import LoginForm, SignupForm
#db imports
from . import User

#/login
@auth.route("/login", methods=["GET", "POST"])
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
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

#/signup
@auth.route("/signup", methods=["GET", "POST"])
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