from flaskapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}')"

class Conditions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pain_areas = db.Column(db.String(60), nullable=False)
    ability = db.Column(db.String(60), nullable=False)
    challenges = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Conditions('{self.pain_areas}', '{self.ability}', '{self.challenges}', '{self.user_id}')"
