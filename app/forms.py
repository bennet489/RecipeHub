from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, SubmitField
from wtforms.validators import Length, DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(),
                                                                     EqualTo(password)])
    submit = SubmitField('signUp')
    
class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')
