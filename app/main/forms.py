from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


from flask_wtf.file import FileField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        

    
class WineForm(FlaskForm):
    description = TextAreaField('Description', validators=[
        DataRequired(), Length(min=1, max=140)])
    rating = SelectField('Rating',choices=[1,2,3,4,5])
    image = FileField('Image')
    submit = SubmitField('Add')
    
class EditWineForm(WineForm):
    submit = SubmitField('Edit')
    delete = SubmitField('Delete',render_kw={'class':'btn-danger'})
    image = FileField('Replace Image')
    delete_image = BooleanField('Delete Image')
    