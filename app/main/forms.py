from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError,  Email, EqualTo
from flask_login import current_user
from app.models import User

class DeviceRegistrationForm(FlaskForm):
    deviceID = IntegerField('Device ID', validators=[DataRequired()])
    submit = SubmitField('Register your device')

    def validate_entry(self, deviceID):
        if not deviceID.isnumeric():
            raise ValidationError('Please enter a number.')

class TestUnlockForm(FlaskForm):
    submit = SubmitField('Register Unlock')
    deviceField = SelectField(u'Devices', choices=[], validators=[DataRequired()])



class EditNameForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submitName = SubmitField('Change Username')

    def __init__(self, original_username, *args, **kwargs):
        super(EditNameForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    #TODO: Fix the hacky strategy in routes.py so this works
    def validate_username(self, username):
        if username.data!= self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class EditPasswordForm(FlaskForm):
    oldpass = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm New Password', validators = [DataRequired(), EqualTo('password')])
    submitPass = SubmitField('Change Password')