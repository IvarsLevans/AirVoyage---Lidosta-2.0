from flask import Blueprint, render_template, redirect, request
from . import db
from . import models
import flask_login
import re
from . import dataManager

views = Blueprint("views", __name__)

@views.route('/')
def index():
  return render_template("index.html", isLoggedIn = flask_login.current_user.is_authenticated)

@views.route('templates/d&aAirport1.html')
def Airport1():
  return render_template("d&aAirport1.html", isLoggedIn = flask_login.current_user.is_authenticated)

@views.route('templates/d&aAirport2.html')
@flask_login.login_required
def Airport2():
  return render_template("d&aAirport2.html", isLoggedIn = flask_login.current_user.is_authenticated)

@views.route('templates/d&aAirport3.html')
def Airport3():
  return render_template("d&aAirport3.html", isLoggedIn = flask_login.current_user.is_authenticated)

@views.route('templates/d&aAirport4.html')
def Airport4():
  return render_template("d&aAirport4.html", isLoggedIn = flask_login.current_user.is_authenticated)

@views.route("data", methods=["GET", "POST"])
def data():
  # if not flask_login.current_user.is_authenticated:
  #   return 'permissionDenied'
  if request.method == 'POST':
    action = request.form.get('action')
    tableName = request.form.get('table')
    key = request.form.get('key')
    fieldName = request.form.get('field')
    value = request.form.get('value')
    success = False
    if action == 'edit':
      success = dataManager.tryEditDatabase(tableName, key, fieldName, value)
    elif action == 'add':
      success = dataManager.tryAddToDatabase(tableName, value)
    elif action == 'delete':
      success = dataManager.tryRemoveFromDatabase(tableName, key)
    if success:
      return 'success'
    else:
      return ''
  else:
    return render_template(
      "data.html",
      isLoggedIn = flask_login.current_user.is_authenticated,
      airports = models.Airport.query.all(),
      airplanes = models.Airplane.query.all(),
      flights = models.Flight.query.all())

@views.route("generate_data")
def generate_data():
  models.Airport.query.delete()
  models.Airplane.query.delete()
  airport = models.Airport(name = "My airport", abbreviation = "MAP", address = "Riga")
  db.session.add(airport)
  airplane = models.Airplane(model='a222', yearOfManufacture = 2000, seats = 200)
  airport = models.Airport(name = "A BIG PLANE", abbreviation = "ABC", address = "France", airplanes = [airplane])
  db.session.add(airport)
  db.session.add(airplane)
  db.session.commit()

  return redirect("data")