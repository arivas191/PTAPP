from flask import render_template, url_for, flash, redirect, request, session
from flaskapp import app, db, bcrypt
from flaskapp.forms import RegistrationForm, LoginForm, ConditionsForm
from flaskapp.models import *
from flaskapp.input_movement import InputMovement
from flaskapp.compute import ComputeMovementMetrics
from flask_login import login_user, current_user, logout_user, login_required
import numpy as np
from openpyxl import load_workbook
import datetime
import csv
from flaskapp.ai import AI

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
            if len(user.challenges):
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
            if len(current_user.challenges) < 2:
                user_condition = current_user.challenges
                is_duplicate=False
                if len(user_condition) > 0:
                    if form.challenges.data == user_condition[0].body_part.value:
                        is_duplicate=True
                if is_duplicate:
                    user_condition.is_duplicate = True
                    db.session.commit()

                condition = Challenge(goal=form.goals.data, level=form.level.data,
                                        body_part=form.challenges.data, user_id=current_user.get_id(), is_duplicate=is_duplicate)
                db.session.add(condition)
                db.session.commit()
            else:
                flash('You can only specify up to two conditions.', 'danger')
            return redirect(url_for('pickexercise'))
    return render_template('conditions.html', form=form)

#endpoint for the exercises page
@app.route('/pickexercise', methods=['GET', 'POST'])
@login_required
def pickexercise():
    if current_user.is_authenticated:
        challenges = current_user.challenges
        if len(challenges) == 0:
            exercises = None
        else:
            exercises = []
            for challenge in challenges:
                exercise = Exercise.query.filter_by(body_part=challenge.body_part).first()
                if challenge.is_duplicate and exercises:
                    break
                else:
                    exercises.append(exercise)
    return render_template('pickexercise.html', exercises=exercises)

#endpoint for the progress page
@app.route('/progress', methods=['GET', 'POST'])
@login_required
def progress():
    # if current_user.is_authenticated:
    #     challenges = current_user.challenges
    #     if len(challenges) == 0:
    #         exercises = None
    #     else:
    #         exercises = []
    #         for challenge in challenges:
    #             exercise = Exercise.query.filter_by(body_part=challenge.body_part).first()
    #             if challenge.is_duplicate and exercises:
    #                 break
    #             else:
    #                 exercises.append(exercise)
    return render_template('progress.html')

#endpoint for the user profile page
@app.route('/profile')
@login_required
def profile():
    challenge = Challenge.query.filter_by(user_id=current_user.get_id()).first()
    form = ConditionsForm()
    # get the history of completed exercises pertaining to the current user
    history = db.session.query(Exercise).join(History, Exercise.id == History.exercise_id). \
                                         add_columns(History.time_stamp). \
                                         filter(History.user_id == current_user.get_id()).all()
    return render_template('profile.html', challenge=challenge, form=form, history=history)

#endpoint for the movement page
@app.route('/movement/<exercise>')
@login_required
def movement(exercise):
    if current_user.is_authenticated:
        movement = Movement(exercise_id=exercise, user_id=current_user.get_id())
        db.session.add(movement)
        db.session.commit()

        #Clear the csv file for a new exercise to be added
        open('flaskapp/static/user_data.csv', 'w').close()

    return render_template('movement.html', movement=movement)
# short-term, "start", create the movement, spinny graphic, stop button,
# long-term user clicks "Start" -> create movement in db, collect the user data, analyze with the calculate api show user a spinny bar "working out..."  add a stop button. When stop is clicked calculate wraps up, updates the movement object, creates a feedback entry and calls feeedback api

#endpoint for the feedback page
@app.route('/feedback/<movement>', methods=['GET', 'POST'])
@login_required
def feedback(movement):
    if current_user.is_authenticated:
        movement = Movement.query.get(movement)
        # if movement.feedback:
        #     # user is viewing a past feedback
        # else:
        # feedback is in-progress
        # create the feedback
        feedback = Feedback(movement_id=movement.id)
        db.session.add(feedback)
        db.session.commit()

        # create a history record for this completed exercise/workout
        history = History(user_id=current_user.get_id(), exercise_id=movement.exercise.id, time_stamp=datetime.datetime.now())
        db.session.add(history)
        db.session.commit()

        #Read in the data from the excel file after the workout has concluded
        movements_list = []

        with open('flaskapp/static/user_data.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            workout = False
            reset = False

            for row in csv_reader:
                if len(row) == 0:
                    continue
                if row[0] == 'reset':
                    workout = True
                elif workout:
                        if len(row) ==2 and not row[1] == '':
                            movements_list.append(InputMovement(datetime.datetime.fromtimestamp(int(row[0])//1000.0).time(), float(row[1])))
        movements_vector = np.array(movements_list)

        calculations = ComputeMovementMetrics(movements_vector)
        calculations.find_max_force()
        calculations.find_repetitions()
        calculations.find_duration()
        #print(calculations.max_force)
        #print(calculations.repetitions)
        #print(calculations.duration)

        user_max_force = calculations.max_force
        user_repetitions = calculations.repetitions
        exercise = movement.exercise.body_part.value

        #Update the movement record with the user's metrics
        movement.max_force = user_max_force
        movement.repetitions_num = user_repetitions
        movement.duration = calculations.duration
        db.session.add(movement)
        db.session.commit()

        #### CALL scikit method here and pass the user's max force, reps and exercise id #####
        print(user_max_force)
        print(user_repetitions)
        print(exercise)
        ai = AI(user_max_force, user_repetitions, exercise) # placeholder value for reps

        strength_feedback = ai.run()
        print(strength_feedback[0])
        print(type(strength_feedback[0]))


        
        

        # call the AI API
    return render_template('feedback.html', feedback=feedback, exercise=exercise,
                            movement=movement, category=strength_feedback, repetitions=user_repetitions,
                            force=user_max_force)
