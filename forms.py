from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField(label='Sign In')

class UserSignupForm(FlaskForm):
    first_name = StringField('First Name', validators = [DataRequired()])
    last_name = StringField('Last Name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired(), Length(8)])
    phone_number = StringField('Phone Number', validators = [DataRequired(), Length(10,12)])
    address = StringField('Address', validators = [DataRequired()])
    submit_button = SubmitField(label='Create an Account')

class ProfileButton(FlaskForm):
    submit_button = SubmitField(label="Edit Profile Details")

class EditProfile(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    phone_number = StringField('Phone Number')
    address = StringField('Address')
    submit_button = SubmitField(label = "Save Changes")