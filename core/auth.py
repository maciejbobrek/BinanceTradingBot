from flask import Blueprint,render_template,redirect,url_for,request,flash
from database import db
from flask_login import UserMixin,login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from db_Models import *
from client_wrapper import client
aut=Blueprint('auth',__name__)
@aut.route('/login',methods=['GET','POST'])
def login():
    """
        Allows user to login using flask LoginManager.
    Returns:
        redirects user to home page if the login proccess was successfull, otherwise redirects to the same login page.
    """
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if User.query.filter_by(email=email).first():
            if check_password_hash(user.password, password):
                flash('Logged in successfully!',category='success')
                login_user(user,remember=True)
                return redirect(url_for('app.index'))
            else:
                flash('Incorrect password,try again',category='error')
        else:
            flash('Email does not exist',category='error')
    return render_template("login.html",user=current_user)


@aut.route('/logout')
@login_required
def logout():
    """
        Allows user to logout, only accessible when user is logged in
    Returns:
        Redirects user to login page    
    """

    client.set_dummy()
    logout_user()
    flash('You were logged out.',category='success')
    return redirect(url_for('auth.login'))



@aut.route('/signup',methods=['GET','POST'])
def signup():
    """
        Allows user to signup using flask LoginManager and parse all the data from user to database using SQLAlchemy. 
    Returns:
        Redirects user to home page, when the proccess was successful. Otherwise it flashes a massage what went wrong in the sign-up proces.  
    """
    if request.method=='POST':
        email=request.form.get('email')
        first_name=request.form.get('firstName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        user=User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.',category='error')
        elif len(email)<4:
            flash('email must be longer than 4 characters!',category='error')
        elif len(first_name)<2:
            flash('first name must be longer than 2 characters!',category='error')
        elif password1 != password2:
            flash('Passwords must be at least 5 characters!',category='error')
        else:
            new_user=User(email=email,first_name=first_name,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!',category='success')
            login_user(new_user)
            return redirect(url_for('app.index'))
    return render_template('signup.html',user=current_user)

