from . import db
import datetime

class Watchlist(db.Model):
    __tablename__ = 'watchlist'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text)
    inserttime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    alert = db.Column(db.Boolean)
    filename = db.Column(db.Text)
    filetime = db.Column(db.DateTime)

    def __repr__(self):
        return '<%r %r>' % (self.type, self.filename)