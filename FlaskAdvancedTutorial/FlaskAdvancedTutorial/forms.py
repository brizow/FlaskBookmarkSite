from flask_wtf import Form
from wtforms.fields import StringField
from flask_wtf.html5 import URLField
from wtforms.validators import DataRequired, url

class BookmarkForm(Form):
    #create fields with more readablility thanks to the jinja macro form
    url = URLField("The URL for your bookmark:", validators=[DataRequired(), url()])
    description = StringField("Add an optional description:")

    #"""This creates a user form for inputting data. This has two fields, url and description"""
    #url = URLField("url", validators=[DataRequired(), url()])
    #description = StringField("description")

    #overrides the default validator
    #if not http:// or https:// then add it to the data.
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
                                    


