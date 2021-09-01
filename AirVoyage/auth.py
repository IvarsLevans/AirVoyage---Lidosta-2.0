from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("templates/login.html", methods=["GET", "POST"])
def login():
    data = request.form
    print(data)
    return render_template ("login.html")

@auth.route("templates/log_out.html")
def log_out():
    return render_template ("login_out.html")

@auth.route("templates/signUp.html", methods=["GET", "POST"])
def signUp():
    if request.method == "POST":
        email = request.form.get('email')
        psw = request.form.get("psw")
        pswRepeat = request.form.get("pswRepeat")

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(psw) < 7:
           flash('Password must be at least 7 characters.', category='error')
        elif pswRepeat != psw:
            flash('Passwords don\'t match.', category='error')
        else:
            # add user to database
            new_user = User(email=email, psw=generate_password_hash(
                psw, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.index'))
            
    return render_template("signUp.html")