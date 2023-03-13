from flask import Flask, render_template, request, flash, redirect, jsonify
from auth import aut
from home import app_home
from db_Models import User
from database import db
from flask_login import LoginManager

from bot_manager import reset_uptime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.secret_key = b'96da9770f9abdb98eb625dfb2247d3ed6a9850bcde9593e40ac3f0dd6c3fd468'

@app.before_first_request
def before_first_request():
    reset_uptime()
app.app_context().push()
db.init_app(app)
db.create_all()
loginmanager=LoginManager()
loginmanager.login_view='auth.login'
loginmanager.init_app(app)
@loginmanager.user_loader
def load_user(id):
    return User.query.get(int(id))
app.register_blueprint(aut,url_prefix='/')
app.register_blueprint(app_home,url_prefix='/')


