from database import db
from flask_login import UserMixin
from sqlalchemy.sql import func
NO_UPTIME = 0.0
class Trade(db.Model):
    db.__tablename__ = "trade" 
    id = db.Column(db.Integer, primary_key=True)
    open_price = db.Column(db.Float)
    close_price = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    bot_id = db.Column(db.Integer, db.ForeignKey('bot.id'))
    capital = db.Column(db.Float)
    
class User(db.Model, UserMixin):
    db.__tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    created_at= db.Column(db.DateTime(timezone=True), default=func.now())
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    bots = db.relationship('Bot')
    
class Bot(db.Model):
    db.__tablename__ = "bot"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    trades = db.relationship('Trade')
    uptime = db.Column(db.Float, default=NO_UPTIME)
    public = db.Column(db.String(150), unique=True)
    secret = db.Column(db.String(150), unique=True)
    keylabel = db.Column(db.String(150), unique=True)
