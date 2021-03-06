from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User

class PostForm(FlaskForm):
    body = TextAreaField("Work Record", validators=[Required()])
    submit = SubmitField('Submit')
