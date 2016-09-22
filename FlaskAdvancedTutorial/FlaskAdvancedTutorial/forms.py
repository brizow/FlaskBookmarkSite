from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from flask_wtf.html5 import URLField
from wtforms.validators import DataRequired, url

class BookmarkForm(Form):
    #create fields with more readablility thanks to the jinja macro form
    url = URLField('Url: ', validators=[DataRequired(), url()])
    description = StringField('Description: ')

    #overrides the default validator
    #if not http:// or https:// then add it to the data.
    #doesn't seem to work on Chrome.
    def validate(self):
        if not self.url.data.startswith("http://") or\
               self.url.data.startswith("https//"):
                self.url.data = "http://" + self.url.data

        #calls the normal validate class on the parent form. Checks for all other errors.
        if not Form.validate(self):
            return False

        #check whether the user typed a description, if not use the url as the description.
        if not self.description.data:
            self.description.data = self.url.data
        
        #if everything checks out return true so the validator 
        #class knows things are good to go.
        return True

#Login form class                                    
class LoginForm(Form):
    username = StringField("Your Username:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in.")
    submit = SubmitField("Log In")

