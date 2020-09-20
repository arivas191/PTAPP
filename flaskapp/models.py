from flaskapp import db, login_manager
from flask_login import UserMixin
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy_imageattach.entity import Image, image_attachment

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    age = db.Column(db.Integer)
    challenges = db.relationship('Challenge', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}')"

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body_part = db.Column('BodyPart', nullable=False)
    goal =  db.Column('Goal', nullable=False)
    level = db.Column('Level', nullable=False)
    exercises = db.relationship('Exercise', backref='purpose', lazy='dynamic')

    def __repr__(self):
        return f"Challenge('{self.body_part}')"

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    description = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(20), unique=True, nullable=False)
    exercise_image = image_attachment('ExerciseImage')
    learn_more_body = db.Column(db.String(160), unique=True, nullable=False)
    movements = db.relationship('Movement', backref='exercise', lazy='dynamic')

    def __repr__(self):
        return f"Exercise('{self.title}')"

class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))
    repetitions_num = db.Column(db.Integer, nullable=False)
    max_distance = db.Column(db.Integer, nullable=False)
    max_force = db.Column(db.Integer, nullable=False)
    steadiness = db.Column('Steadiness', nullable=False)

    def __repr__(self):
        return f"Movement('{self.exercise.title}')"

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movement_id = db.Column(db.Integer, db.ForeignKey('movement.id'))
    statement = db.Column(db.String(80), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    delivered = db.Column(db.Boolean, nullable=False)

class BodyPart(Enum):
    Arm = 1
    Leg = 2
    Hand = 3
    Ankle = 4
    Shoulder = 5
    Hips = 6
    Knee = 7

class Level(Enum):
    Beginner = 1
    Intermediate = 2
    Advanced = 3

class Goal(Enum):
    Stability = 1
    Strength = 2
    Endurance = 3
    PainRelief = 4

class ExerciseImage(Image):
    """Exerise image model"""

    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), primary_key=True)
    exercise = db.relationship('Exercise')

class Steadiness(Enum):
    VeryShaky = 1
    Shaky = 2
    Neutral = 3
    Steady = 4
    VerySteady = 5
    