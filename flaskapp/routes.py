from flask import render_template, url_for, flash, redirect, request
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
            if user.challenges.count():
                return redirect(url_for('pickexercise'))
            else:
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
    if current_user.is_authenticated:
        form = ConditionsForm()
        if form.validate_on_submit():            
            if current_user.challenges.count() > 0:
                challenge = Challenge.query.filter_by(user_id=current_user.get_id()).update(dict(goal=form.goals.data, level=form.level.data, body_part=form.challenges.data))
                db.session.commit()
                return redirect(url_for('pickexercise'))
            # if current_user.challenges.count() < 2:
                # user_condition = current_user.challenges.first()
                # is_duplicate=False
                # if user_condition is not None: 
                #     if form.challenges.data == user_condition.body_part.value:
                #         is_duplicate=True
                # if is_duplicate:
                #     user_condition.is_duplicate = True
                #     db.session.commit()
            elif current_user.challenges.count() == 0:
                is_duplicate = False
                condition = Challenge(goal=form.goals.data, level=form.level.data,
                                        body_part=form.challenges.data, user_id=current_user.get_id(), is_duplicate=is_duplicate)
                db.session.add(condition)
                db.session.commit()
                return redirect(url_for('pickexercise'))
            else:
                flash('You can only specify up to two conditions.', 'danger')
    return render_template('conditions.html', form=form)

#endpoint for the exercises page
@app.route('/pickexercise', methods=['GET', 'POST'])
@login_required
def pickexercise():
    if current_user.is_authenticated and current_user.challenges:
        challenges = current_user.challenges
        exercises = []
        for challenge in challenges:
            exercise = Exercise.query.filter_by(body_part=challenge.body_part).first()
            if challenge.is_duplicate and exercises:
                break
            else:
                exercises.append(exercise)
    return render_template('pickexercise.html', exercises=exercises)

#endpoint for the user profile page
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        if current_user.is_authenticated:
            challenge = Challenge.query.filter_by(user_id=current_user.get_id()).first()
            form = ConditionsForm()
            form.goals.data = challenge.goal
            return render_template('profile.html', level=challenge.level.name, goal=challenge.goal.name, body_part=challenge.body_part, form=form)
    elif request.method == 'POST':
        if current_user.is_authenticated:
            challenge = Challenge.query.filter_by(user_id=current_user.get_id()).first()
            form = ConditionsForm()
            if form.validate_on_submit():            
                if current_user.challenges.count() > 0:
                    challenge = Challenge.query.filter_by(user_id=current_user.get_id()).update(dict(goal=form.goals.data, level=form.level.data, body_part=form.challenges.data))
                    db.session.commit()
                    return redirect(url_for('profile'))
                elif current_user.challenges.count() == 0:
                    is_duplicate = False
                    condition = Challenge(goal=form.goals.data, level=form.level.data,
                                            body_part=form.challenges.data, user_id=current_user.get_id(), is_duplicate=is_duplicate)
                    db.session.add(condition)
                    db.session.commit()
                    return redirect(url_for('profile'))
                else:
                    flash('You can only specify up to two conditions.', 'danger')
        # return render_template('conditions.html', form=form)
        return render_template('profile.html', form=form)
