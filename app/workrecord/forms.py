#coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, DateTimeField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User
from flask_pagedown.fields import PageDownField

class PostForm(FlaskForm):
    body = PageDownField(u"工作日志", validators=[Required()])
    worktype = SelectField(u"类型",choices=[(u'巡视',u'巡视'),(u'维护',u'维护')])
    event_starttime = DateTimeField(format='%H%M')
    submit = SubmitField(u'提交')
