from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from . import dataManager

auth = Blueprint("auth", __name__)

@auth.route("templates/login.html", methods=["GET", "POST"])
def login():
  if current_user.is_authenticated:
     return redirect(url_for('views.index'))
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('psw')
    user = User.query.filter_by(email = email).first()
    if(user is not None and check_password_hash(user.psw, password)):
      login_user(user)
      return redirect(url_for('views.index'))
  return render_template ("login.html",
    isLoggedIn = current_user.is_authenticated,
    isAdmin = dataManager.isAdmin(current_user))

@auth.route("templates/log_out.html")
def log_out():
  logout_user()
  return redirect(url_for('views.index'))

@auth.route("templates/signUp.html", methods=["GET", "POST"])
def signUp():
  if current_user.is_authenticated:
     return redirect(url_for('views.index'))
  if request.method == "POST":
    name = request.form.get('name')
    surname = request.form.get('surname')
    email = request.form.get('email')
    psw = request.form.get("psw")
    pswRepeat = request.form.get("pswRepeat")

    if len(email) < 4:
      flash('Email must be greater than 3 characters.', category='error')
    elif len(psw) < 7:
      flash('Password must be at least 7 characters.', category='error')
    elif pswRepeat != psw:
      flash('Passwords don\'t match.', category='error')
    elif User.query.filter_by(email = email).first() is not None:
      flash('Email already taken.', category='error')
    elif len(name) < 2:
      flash('Name must be greater than 1 characters.', category='error')
    elif len(surname) < 2:
      flash('Surname must be greater than 1 characters.', category='error')
    elif ' ' in name or ' ' in surname:
      flash('Name and surname can not contain wihtespaces.', category='error')
    else:
      # add user to database
      new_user = User(name=name, surname=surname, email=email, psw=generate_password_hash(
          psw, method='sha256'))
      db.session.add(new_user)
      db.session.commit()
      login_user(new_user, remember=True)
      flash('Account created!', category='success')
      return redirect(url_for('views.index'))
  return render_template("signUp.html",
    isLoggedIn = current_user.is_authenticated,
    isAdmin = dataManager.isAdmin(current_user))
