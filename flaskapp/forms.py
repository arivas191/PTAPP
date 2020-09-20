from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flaskapp.models import *

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username already exists.')

class LoginForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class ConditionsForm(FlaskForm):
    challenges = SelectField('Area', validators=[DataRequired()],
                            choices=[(choice.name, choice.value) for choice in BodyPart])
    goals = SelectField('Goal', validators=[DataRequired()],
                            choices=[(choice.name, choice.value) for choice in Goal])
    level = SelectField('Exercise Ability', validators=[DataRequired()],
                            choices=[(choice.name, choice.value) for choice in Level])
    submit = SubmitField('Submit')
