#coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, DateTimeField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User
from flask_pagedown.fields import PageDownField

types = [
	(u'巡视',u'巡视'),
	(u'维护',u'维护'),
	(u'维修',u'维修')
	]

tags = [
	(u'A001',u'A001'),
	(u'A002',u'A002'),
	(u'A003',u'A003')
	]

class PostForm(FlaskForm):
    worktype = SelectField(u"工作类型", choices=types)
    worktag = SelectField(u'标签', choices=tags)
    event_starttime = DateTimeField(u'开始时间(UTC)', format='%H%M')
    event_endtime = DateTimeField(u'结束时间(UTC)', format='%H%M')
    body = PageDownField(u"工作日志", validators=[Required()])
    submit = SubmitField(u'提交')
