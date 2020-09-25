from flask import render_template, url_for, flash, redirect
from flaskapp import app, db, bcrypt
from flaskapp.forms import RegistrationForm, LoginForm, ConditionsForm
from flaskapp.models import *
from flask_login import login_user, current_user, logout_user, login_required

#endpoint for the home page
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

#endpoint for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('conditions'))
        else:
            flash('Username or password is incorrect.', 'danger')
    return render_template('login.html', form=form)

#endpoint for the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

#endpoint for logging out the user, goes to the homepage
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

#endpoint for the conditions page
@app.route('/conditions', methods=['GET', 'POST'])
@login_required
def conditions():
    form = ConditionsForm()
    if form.validate_on_submit():
        conditions = Challenge(goal=form.goals.data, level=form.level.data,
                                body_part=form.challenges.data, user_id=current_user.get_id())
        db.session.add(conditions)
        db.session.commit()
        return redirect(url_for('pickexercise'))
    return render_template('conditions.html', form=form)

#endpoint for the exercises page
@app.route('/pickexercise', methods=['GET', 'POST'])
@login_required
def pickexercise():
    if current_user.is_authenticated:
        user_id = current_user.get_id()
        challenge = Challenge.query.filter_by(user_id=user_id).first()
        print(challenge.body_part)
        print(challenge.goal)
        print(challenge.level)
    return render_template('pickexercise.html')
