from . import db
from flask import url_for
import datetime

class Watchlist(db.Model):
	__tablename__ = 'watchlist'
	id = db.Column(db.Integer, primary_key=True)
	prd_type = db.Column(db.Text)
	inserttime = db.Column(db.DateTime, default=datetime.datetime.now())
	alert = db.Column(db.Boolean)
	filename = db.Column(db.Text)
	filetime = db.Column(db.DateTime)
