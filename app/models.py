from . import db

class Watchlist(db.Model):
	__tablename__ = 'watchlist'
	id = db.Column(db.Integer, primary_key=True)
	prd_type = db.Column(db.Text)
	inserttime = db.Column(db.String)
	alert = db.Column(db.Boolean)
	filename = db.Column(db.Text)
	filetime = db.Column(db.DateTime)
