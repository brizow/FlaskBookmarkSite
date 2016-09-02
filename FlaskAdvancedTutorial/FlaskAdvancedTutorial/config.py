#import our base path for postgres
#basedir = os.path.abspath(os.path.dirname(__file__))
#setup the secret session key. Not sure this is the preferred way.
app.secret_key = '\x1f\x9b\xfb\x83"n\x16\xf5y\xc5{\xf6i\xd1\xb0\x81h_p\xd6e\xa0\xea'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://user:user123@localhost/fat"
#"postgresql://" + os.path.join(basedir, "fat.db")