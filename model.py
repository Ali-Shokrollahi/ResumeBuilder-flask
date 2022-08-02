from . import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    job = db.Column(db.String(30))
    description = db.Column(db.Text())
    password = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True)
    number = db.Column(db.String(11), unique=True)
    gender = db.Column(db.String(11))
    age = db.Column(db.String(10))
    join_date = db.Column(db.DateTime, default=datetime.now().date())
    photo = db.Column(db.String(50))
    isallowed = db.Column(db.BOOLEAN(), default=False)
    iscreated = db.Column(db.BOOLEAN(), default=False)
    resumeproccess = db.Column(db.Integer, default=0)
    maxpoint = db.Column(db.Integer, default=20)
    point = db.Column(db.Integer, default=0)

    workdata = db.relationship('WorkData', backref='workdata')
    experience = db.relationship('Experience', backref='experience')
    education = db.relationship('Education', backref='education')
    social = db.relationship('Social', backref='social')
    skill = db.relationship('Skill', backref='skill')

    def __repr__(self):
        return self.name + " " + self.lastname


class Social(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instagram = db.Column(db.String(30))
    telegram = db.Column(db.String(30))
    linkedin = db.Column(db.String(30))
    github = db.Column(db.String(30))
    pinterest = db.Column(db.String(30))
    address = db.Column(db.Text())
    maxpoint = db.Column(db.Integer, default=10)
    point = db.Column(db.Integer, default=0)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))


class WorkData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    experience = db.Column(db.Integer, nullable=False)
    projects_number = db.Column(db.Integer, nullable=False)
    customer_number = db.Column(db.Integer, nullable=False)
    maxpoint = db.Column(db.Integer, default=10)
    point = db.Column(db.Integer, default=0)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))


class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    company = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text())
    duration = db.Column(db.Integer)
    maxpoint = db.Column(db.Integer, default=25)
    point = db.Column(db.Integer, default=0)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))


class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    school = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text())
    duration = db.Column(db.Integer)
    maxpoint = db.Column(db.Integer, default=15)
    point = db.Column(db.Integer, default=0)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    percent = db.Column(db.Integer, nullable=False, default=0)
    maxpoint = db.Column(db.Integer, default=20)
    point = db.Column(db.Integer, default=0)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
