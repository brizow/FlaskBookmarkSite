"""
Routes and views for the flask application.
"""
import os
from datetime import datetime
#request allows us to use if request.method == "POST" because it is bound to a view
#flash allows us to use session messages. However we will need to set a secret key.
from flask import render_template, url_for, Flask, request, redirect, flash

#import our form class
from forms import BookmarkForm

from FlaskAdvancedTutorial import app


#setup the secret session key. Not sure this is the preferred way.
app.secret_key = '\x1f\x9b\xfb\x83"n\x16\xf5y\xc5{\xf6i\xd1\xb0\x81h_p\xd6e\xa0\xea'
#creating a global list for now. Not recommended because multiple connections using the same global is asking for trouble.
#we will learn about databasing next module.
bookmarks = []

def store_bookmark(url, description):
    bookmarks.append(dict(
        url = url,
        description = description,
        user = "brett",
        date = datetime.now()
    ))

def new_bookmarks(num):
    return sorted(bookmarks, key=lambda bm: bm["date"], reverse=True)[:num]

#/home view
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        new_bookmarks = new_bookmarks(5)
    )

#/add view
@app.route("/add", methods=["GET", "POST"])
def add():
    #we are using the form we created in forms.py
    form = BookmarkForm()
    if form.validate_on_submit(): #checks http form or validation errors
        #otherwise lets add the data
        url = form.url.data
        description = form.description.data
        store_bookmark(url, description)
        flash("Stored '{}'".format(description))
        return redirect(url_for("home"))

    #if request.method == "POST":
    #    url = request.form["url"]
    #    store_bookmark(url)
    #    flash("Stored bookmark '{}'".format(url))
    #    return redirect(url_for("home"))

    #if there are error just rerender the form again
    return render_template("add.html", form=form)

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )



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
