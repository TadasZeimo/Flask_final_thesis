import os
import time
from datetime import datetime
import math
from flask import Flask, render_template, flash, url_for, redirect, request, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from forms import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, logout_user, current_user, login_user, UserMixin

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.app_context().push()

app.config['SECRET_KEY'] = 'vslkhfweigfwei/:6496413.'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'dataBase.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Login, logout

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = None


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# ----------------------------------------------------------------------------------------------------------------------------------

db = SQLAlchemy(app)
Migrate(app, db)

# Data base tables


class Mountaineers(db.Model):
    __tablename__ = 'Mountaineers'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80), nullable=False)
    lname = db.Column(db.String(80), nullable=False)
    fotoUrl = db.Column(db.Text, nullable=False)
    biography = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(80))

    def __init__(self, fname, lname, fotoUrl, biography, date):
        self.fname = fname
        self.lname = lname
        self.fotoUrl = fotoUrl
        self.biography = biography
        self.date = date

    def __repr__(self):
        return f'{self.fname}'


class Users(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(320), nullable=False)
    password = db.Column(db.String(127), nullable=False)
    date = db.Column(db.String(80))

    def __init__(self, userName, email, password, date):
        self.userName = userName
        self.email = email
        self.password = password
        self.date = date

    def __repr__(self):
        return f'{self.id}'


# db.create_all()
# ----------------------------------------------------------------------------------------------------------------------------------
