import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension

#initialize the database object
db = SQLAlchemy()

#configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"

#add flask debug toolbar
toolbar = DebugToolbarExtension()

#for displaying nice js timestamps
moment = Moment()

class Config:
    SECRET_KEY = '\x1f\x9b\xfb\x83"n\x16\xf5y\xc5{\xf6i\xd1\xb0\x81h_p\xd6e\xa0\xea'
    DEBUG = False

class DevelopmentConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://user:user123@localhost/fat"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://user:user123@localhost/fat_test"
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql://user:user123@localhost/fat"

config_by_name = dict(
    dev = DevelopmentConfig,
    test = TestingConfig,
    prod = ProductionConfig)