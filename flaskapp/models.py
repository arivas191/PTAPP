from flaskapp import db, login_manager
from flask_login import UserMixin
from sqlalchemy import Integer, Enum, Unicode
import enum
from sqlalchemy.orm import relationship
from sqlalchemy_imageattach.entity import Image, image_attachment

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class BodyPart(enum.Enum):
    Arm = 'Arm'
    Leg = 'leg'
    Hand = 'Hand'
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

class ExerciseImage(db.Model, Image):
    """Exerise image model"""

    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), primary_key=True)
    exercise = db.relationship('Exercise')

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
    # age = db.Column(db.Integer)
    challenges = db.relationship('Challenge', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.id}', '{self.username}')"

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body_part = db.Column(Enum(BodyPart), nullable=False)
    goal =  db.Column(Enum(Goal), nullable=False)
    level = db.Column(Enum(Level), nullable=False)
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
    steadiness = db.Column(Enum(Steadiness), nullable=False)

    def __repr__(self):
        return f"Movement('{self.exercise.title}')"

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movement_id = db.Column(db.Integer, db.ForeignKey('movement.id'))
    statement = db.Column(db.String(80), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    delivered = db.Column(db.Boolean, nullable=False)
