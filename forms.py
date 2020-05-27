from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError



class Log_in_form(FlaskForm):
    email = StringField('Email', validators=[Email(message='^This field must be Email.'), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class Sign_up_form(FlaskForm):
    email = StringField('Email', validators=[Email(message='^This field must be Email.'), DataRequired()])
    name = StringField('User name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm', validators=[EqualTo('password', message='^This field must be Equal to password')])
    submit = SubmitField('Register')


class New_note(FlaskForm):

    information = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Add')


class Edit_user(FlaskForm):

    email = StringField('Email')
    name = StringField('User name', validators=[DataRequired()])
    submit = SubmitField('Edit')


class Edit_note(FlaskForm):

    submit = SubmitField('Edit')