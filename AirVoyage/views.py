from flask import Blueprint, render_template, redirect, request, flash
from . import db
from . import models
import flask_login
from . import dataManager
from datetime import datetime

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
  # for user in models.User.query.all():
  #   print(user.tickets)
  if request.method == 'POST':
    if request.form.get('action') == 'filter':
      # TODO (only from filter)
      dateFrom = request.form.get('dateFrom')
      dateTo = request.form.get('dateTo')
      airportFrom = request.form.get('from')
      airportTo = request.form.get('to')
      queries = []
      if airportFrom != 'any':
        queries.append(models.Flight.airportFromId == airportFrom)
      if airportTo != 'any':
        queries.append(models.Flight.airportToId == airportTo)
      if dateFrom != ' ':
        queries.append(models.Flight.departureDate > dateFrom)
      if dateTo != ' ':
        queries.append(models.Flight.arrivalDate < dateTo)
      print(f'a{dateFrom}a')
      print(*queries)
      flights = db.session.query(models.Flight).filter(*queries).all()
      head = "<tr><th>From</th><th>To</th><th>Departure date</th><th>Arrival</th><th>Airplane</th></tr>"
      return head + "".join([f'<tr value=\"{flight.id}\"><td>{flight.airportFrom.address}</td><td>{flight.airportTo.address}</td><td>{flight.departureDate}</td><td>{flight.arrivalDate}</td><td><button class="book">Book</button></td></tr>' for flight in flights])
    elif request.form.get('action') == 'book':
      ticketId = 0
      if len(models.Ticket.query.all()) > 0:
        ticketId = models.Ticket.query.order_by(-models.Ticket.id).first().id + 1
      flightId = request.form.get('flightId')
      for ticket in flask_login.current_user.tickets:
        if ticket.flightId == int(flightId):
          return 'error'
      if models.Flight.query.filter_by(id = flightId).first() is None:
        return "error"
      else:
        db.session.add(models.Ticket(
          id = ticketId,
          ownerId = flask_login.current_user.id,
          flightId = flightId))
        db.session.commit()
        return "success"
      return "error"
  elif request.method == 'GET':
    return render_template("booking.html",
      isLoggedIn = flask_login.current_user.is_authenticated,
      isAdmin = dataManager.isAdmin(flask_login.current_user),
      flights = db.session.query(models.Flight).all(),
      airports = models.Airport.query.all())

@views.route('myTickets', methods=["GET", "POST"])
@flask_login.login_required
def myTickets():
  if request.method == "POST":
    if request.form.get('action') == 'cancel':
      ticketId = request.form.get('ticketId')
      db.session.query(models.Ticket).filter((models.Ticket.id == ticketId) & (models.Ticket.ownerId == flask_login.current_user.id)).delete()
      db.session.commit()
      return "success"
    return "error"
  return render_template("myTickets.html",
    isLoggedIn = flask_login.current_user.is_authenticated,
    isAdmin = dataManager.isAdmin(flask_login.current_user),
    user = flask_login.current_user)

@views.route("data", methods=["GET", "POST"])
@flask_login.login_required
def data():
  #models.Ticket.__table__.drop(db.engine)
  #models.Airport.__table__.drop(db.engine)
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
@flask_login.login_required
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

@views.route("statistics", methods=["GET", "POST"])
@flask_login.login_required
def statistics():
  if not dataManager.isAdmin(flask_login.current_user):
    return 'permissionDenied'
  return render_template("statistics.html", flights = models.Flight.query.all())