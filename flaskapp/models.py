from flaskapp import db, login_manager
from flask_login import UserMixin
from sqlalchemy import Integer, Enum, Unicode
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
    challenges = db.relationship('Challenge', backref='User', lazy='dynamic')
    movements = db.relationship('Movement', backref='User', lazy='dynamic')

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
    movements = db.relationship('Movement', backref='Exercise', lazy='dynamic')

    def __repr__(self):
        return f"Exercise('{self.title}')"

    def __init__(self, id, description, title, body_part, image_name, learn_more_body=None):
        self.id = id
        self.description = description
        self.title = title
        self.body_part = body_part
        self.image_name = image_name
        if learn_more_body:
            self.learn_more_body = learn_more_body

class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    repetitions_num = db.Column(db.Integer)
    max_distance = db.Column(db.Integer)
    max_force = db.Column(db.Integer)
    steadiness = db.Column(Enum(Steadiness))
    feedback = db.relationship('Feedback', backref='Movement', lazy='dynamic')

    def __repr__(self):
        return f"Movement('{self.user_id}')"

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movement_id = db.Column(db.Integer, db.ForeignKey('movement.id'))
    statement = db.Column(db.String(80), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    delivered = db.Column(db.Boolean, nullable=False)
