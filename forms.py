from flask_wtf import Form 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(Form):
    name = StringField('Name', validators=[DataRequired("Please enter your name.")])
    age = StringField('Age', validators=None)
    phone = StringField('Contact', validators=[DataRequired("Please enter your contact number.")])
    email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
    pword = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
    submit = SubmitField('Register')

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
    pword = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
    submit = SubmitField("Sign in")

class CompanyForm(Form):
    company = StringField('Company Name', validators=None)
    submit = SubmitField('Submit')
