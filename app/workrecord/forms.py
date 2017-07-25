from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User
from flask_pagedown.fields import PageDownField

class PostForm(FlaskForm):
    body = PageDownField("Work Record", validators=[Required()])
    submit = SubmitField('Submit')
