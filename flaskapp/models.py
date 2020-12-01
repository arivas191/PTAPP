from flaskapp import db, login_manager
import datetime
from flask_login import UserMixin
from sqlalchemy import Integer, Enum, Unicode, DateTime
import enum
from sqlalchemy.orm import relationship

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class BodyPart(enum.Enum):
    Arm = 'Arm'
    Ankle = 'Ankle'
    Shoulder = 'Shoulder'
    Hips = 'Hips'
    Knee = 'Knee'

class Level(enum.Enum):
    Beginner = 'Beginner'
    Intermediate = 'Intermediate'
    Advanced = 'Advanced'

class Goal(enum.Enum):
    Stability = 'Stability'
    Strength = 'Strength'
    Endurance = 'Endurance'
    PainRelief = 'Pain relief'

class Steadiness(enum.Enum):
    VeryShaky = 'Very Shaky'
    Shaky = 'Shaky'
    Neutral = 'Neutral'
    Steady = 'Steady'
    VerySteady = 'Very steady'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    challenges = db.relationship('Challenge', backref='user')
    movements = db.relationship('Movement', backref='user')

    def __repr__(self):
        return f"User('{self.id}', '{self.username}')"

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body_part = db.Column(Enum(BodyPart), nullable=False)
    goal =  db.Column(Enum(Goal), nullable=False)
    level = db.Column(Enum(Level), nullable=False)
    is_duplicate = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Challenge('{self.id}', '{self.body_part}', '{self.goal}', '{self.level}')"

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1055), unique=True, nullable=False)
    title = db.Column(db.String(40), unique=True, nullable=False)
    image_name = db.Column(db.String(40), nullable=False)
    learn_more_body = db.Column(db.String(160), unique=True, nullable=True)
    body_part = db.Column(Enum(BodyPart), nullable=False)
    demo_link = db.Column(db.String, nullable=False)
    movements = db.relationship('Movement', backref='exercise')

    def __repr__(self):
        return f"Exercise('{self.title}')"

    def __init__(self, id, description, title, body_part, image_name, demo_link, learn_more_body=None):
        self.id = id
        self.description = description
        self.title = title
        self.body_part = body_part
        self.image_name = image_name
        self.demo_link = demo_link
        if learn_more_body:
            self.learn_more_body = learn_more_body

# table that represents the user's completed workouts. Each row is representative of a completed workout for a given user
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    time_stamp = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"History('{self.user_id}', '{self.exercise_id}', '{self.time_stamp}')"

class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    repetitions_num = db.Column(db.Integer)
    max_distance = db.Column(db.Integer)
    max_force = db.Column(db.Integer)
    duration = db.Column(db.Interval)
    steadiness = db.Column(Enum(Steadiness))
    feedback = db.relationship('Feedback', uselist=False, backref='movement')

    def __repr__(self):
        return f"Movement('{self.id}', '{self.user_id}', '{self.exercise_id}', '{self.exercise.title}', '{self.repetitions_num}', '{self.max_force}', '{self.duration}')"

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movement_id = db.Column(db.Integer, db.ForeignKey('movement.id'), nullable=False)
    statement = db.Column(db.String(80))
    score = db.Column(db.Integer)
