# import web elements from WTF
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length

#Create a class for the web elements needed for a Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# Ceate a class for logging a weather sighting event
# the user is taken from the login session, so there is no username field here
# the Length limits match the column sizes in the sightings table
class SightingForm(FlaskForm):
    city = StringField('City / Location', validators=[DataRequired(), Length(max=30)])
    weather_type = SelectField('Weather Condition', choices=[
        ('Heavy Rain', 'Heavy Rain'),
        ('Storm', 'Storm'),
        ('Fog', 'Fog'),
        ('High Winds', 'High Winds')
    ])
    summary = TextAreaField('Summary / Comments', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Submit Event')
