"""
Routes and views for the authentication methods.
"""
#system imports
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user
#class imports
from . import bookmarks
from . import db
#import our form class
from . import BookmarkForm
#db imports
from . import User, Bookmark, Tag

#/add view
@bookmark.route("/add", methods=["GET", "POST"])
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
        return redirect(url_for("main.home"))
    
    #GET
    #if not validate on submit, show the new form.
    return render_template("add.html", form=form, 
                           title="Bookmark Saver",
                           year=datetime.now().year)

#/edit/bookmarkid 
@bookmark.route("/edit/<int:bookmark_id>", methods=["GET", "POST"])
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
        return redirect(url_for(".user", username=current_user.username))
    return render_template("bookmark_form.html", form=form, title="Edit Bookmark", 
                           year=datetime.now().year)

#/delete/bookmarkid 
@bookmark.route("/delete/<int:bookmark_id>", methods=["GET", "POST"])
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
        return redirect(url_for(".user", username=current_user.username))
    else:
        flash("Please confirm bookmark deletion.")
    return render_template("confirm_delete.html", bookmark=bookmark, nolinks=True)


#/user/username
@bookmark.route("/user/<username>")
@login_required
def user(username):
    #find the first username matching or return 404
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user.html", user=user, 
                           title = "Saved Bookmarks", 
                           year=datetime.now().year)

#/tag/name
@bookmark.route("/tag/<name>")
def tag(name):
    #try to retrieve a tag by name, if none 404, otherwise return template
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template("tag.html", tag=tag, title = "Tags Listing",
                           year=datetime.now().year)
