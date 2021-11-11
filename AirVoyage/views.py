from flask import Blueprint, render_template, redirect, request
from . import db
from . import models
import flask_login
from . import dataManager

views = Blueprint("views", __name__)

@views.route('/')
def index():
  return render_template("index.html", isLoggedIn = flask_login.current_user.is_authenticated, isAdmin = dataManager.isAdmin(flask_login.current_user))

@views.route('templates/d&aAirport1.html')
def Airport1():
  return render_template("d&aAirport1.html", isLoggedIn = flask_login.current_user.is_authenticated, isAdmin = dataManager.isAdmin(flask_login.current_user))

@views.route('templates/d&aAirport2.html')
def Airport2():
  return render_template("d&aAirport2.html", isLoggedIn = flask_login.current_user.is_authenticated, isAdmin = dataManager.isAdmin(flask_login.current_user))

@views.route('templates/d&aAirport3.html')
def Airport3():
  return render_template("d&aAirport3.html", isLoggedIn = flask_login.current_user.is_authenticated, isAdmin = dataManager.isAdmin(flask_login.current_user))

@views.route('templates/d&aAirport4.html')
def Airport4():
  return render_template("d&aAirport4.html", isLoggedIn = flask_login.current_user.is_authenticated, isAdmin = dataManager.isAdmin(flask_login.current_user))

@views.route('booking', methods=["GET", "POST"])
@flask_login.login_required
def booking():
  if request.method == 'POST':
    return 'a'
  elif request.method == 'GET':
    return render_template("booking.html",
      isLoggedIn = flask_login.current_user.is_authenticated,
      isAdmin = dataManager.isAdmin(flask_login.current_user),
      flights = models.Flight.query.all(),
      airports = models.Airport.query.all())

@views.route('myTickets')
@flask_login.login_required
def myTickets():
  return render_template("myTickets.html",
    isLoggedIn = flask_login.current_user.is_authenticated,
    isAdmin = dataManager.isAdmin(flask_login.current_user),
    user = flask_login.current_user)

@views.route("data", methods=["GET", "POST"])
def data():
  #models.Flight.__table__.drop(db.engine)
  #print(models.Airplane.query[1].airport.name)
  if not dataManager.isAdmin(flask_login.current_user):
    return 'permissionDenied'
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
      isAdmin = dataManager.isAdmin(flask_login.current_user),
      airports = models.Airport.query.all(),
      airplanes = models.Airplane.query.all(),
      flights = models.Flight.query.all())

@views.route("generate_data")
def generate_data():
  if not dataManager.isAdmin(flask_login.current_user):
    return 'permissionDenied'
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