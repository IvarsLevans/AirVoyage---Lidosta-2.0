from flask import Blueprint, render_template, redirect, request, flash
from . import db
from . import models
import flask_login
from datetime import datetime

views = Blueprint("views", __name__)

def isAdmin(user):
  admins = ['admin@admin.admin']
  if user.is_authenticated and user.email in admins:
    return True
  else:
    return False

@views.route('/')
def index():
  return render_template("index.html", isLoggedIn = flask_login.current_user.is_authenticated, isAdmin = isAdmin(flask_login.current_user))

@views.route('templates/d&aAirport1.html')
def Airport1():
  return render_template("d&aAirport1.html", isLoggedIn = flask_login.current_user.is_authenticated, isAdmin = isAdmin(flask_login.current_user))

@views.route('templates/d&aAirport2.html')
def Airport2():
  return render_template("d&aAirport2.html", isLoggedIn = flask_login.current_user.is_authenticated, isAdmin = isAdmin(flask_login.current_user))

@views.route('templates/d&aAirport3.html')
def Airport3():
  return render_template("d&aAirport3.html", isLoggedIn = flask_login.current_user.is_authenticated, isAdmin = isAdmin(flask_login.current_user))

@views.route('templates/d&aAirport4.html')
def Airport4():
  return render_template("d&aAirport4.html", isLoggedIn = flask_login.current_user.is_authenticated, isAdmin = isAdmin(flask_login.current_user))

@views.route('booking', methods=["GET", "POST"])
@flask_login.login_required
def booking():
  # for user in models.User.query.all():
  #   print(user.tickets)
  if request.form.get('action') == 'book':
      ticketId = 0
      if len(models.Ticket.query.all()) > 0:
        ticketId = models.Ticket.query.order_by(-models.Ticket.id).first().id + 1
      flightId = request.form.get('flightId')
      for ticket in flask_login.current_user.tickets:
        if ticket.flightId == int(flightId):
          return 'error'
      if models.Flight.query.get(flightId) is None:
        return "error"
      else:
        db.session.add(models.Ticket(
          id = ticketId,
          ownerId = flask_login.current_user.id,
          flightId = flightId,
          purchaseDate = datetime.now()))
        db.session.commit()
        return "success"
      return "error"
  elif request.method == 'GET':
    return render_template("booking.html",
      isLoggedIn = flask_login.current_user.is_authenticated,
      bookedFlightIds = [ticket.flightId for ticket in flask_login.current_user.tickets],
      isAdmin = isAdmin(flask_login.current_user),
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
    isAdmin = isAdmin(flask_login.current_user),
    user = flask_login.current_user,
    tickets = [ticket for ticket in flask_login.current_user.tickets if ticket.flight and not ticket.flight.isFinished])

@views.route('myTickets/<sortOrder>', methods=["GET", "POST"])
@flask_login.login_required
def myTicketsOrdered(sortOrder):
  tickets = flask_login.current_user.tickets
  if sortOrder == "oldest":
    tickets.sort(key = ticketSorter)
  elif sortOrder == "newest":
    tickets.sort(reverse=True, key = ticketSorter)
  return render_template("myTickets.html",
    isLoggedIn = flask_login.current_user.is_authenticated,
    isAdmin = isAdmin(flask_login.current_user),
    user = flask_login.current_user,
    tickets = [ticket for ticket in flask_login.current_user.tickets if ticket.flight and not ticket.flight.isFinished],
    order = sortOrder)
def ticketSorter(e):
  return e.purchaseDate

@views.route("data", methods=["GET", "POST"])
@flask_login.login_required
def data():
  #print(models.Flight.query.get('2'))
  #models.Ticket.__table__.drop(db.engine)
  #models.Airport.__table__.drop(db.engine)
  if not isAdmin(flask_login.current_user):
    return 'permissionDenied'
  
  if request.method == 'POST':
    action = request.form.get('action')
    tableName = request.form.get('table')
    key = request.form.get('key')
    fieldName = request.form.get('field')
    value = request.form.get('value')
    entry = None
    

    if action == 'delete':
      if tableName == 'airports':
        models.Airport.query.filter_by(abbreviation = key).delete()
      elif tableName == 'airplanes':
        models.Airplane.query.filter_by(id = int(key)).delete()
      elif tableName == 'flights':
        models.Flight.query.filter_by(id = int(key)).delete()
      db.session.commit()
      return 'success'
    elif action == 'editRow':
      fieldCount = int(request.form.get('fieldCount'))
      if tableName == 'airports':
        entry = models.Airport.query.get(key)
      elif tableName == 'airplanes':
        entry = models.Airplane.query.get(int(key))
      elif tableName == 'flights':
        entry = models.Flight.query.get(int(key))
      try:
        for i in range(fieldCount):
          fieldName = request.form.get(f'fieldName{i}')
          value = request.form.get(f'value{i}')
          setattr(entry, fieldName, value)
          db.session.commit()
      except AssertionError as e:
        return str(e)
      except:
        return 'error'
      return 'success'
    elif action == 'addRow':
      fieldCount = int(request.form.get('fieldCount'))
      try:
        values = {}
        for i in range(fieldCount):
          values[request.form.get(f'fieldName{i}')] = request.form.get(f'value{i}')
        if tableName == 'airports':
          db.session.add(models.Airport(**values))
        elif tableName == 'airplanes':
          db.session.add(models.Airplane(**values))
        elif tableName == 'flights':
          db.session.add(models.Flight(**values))
        db.session.commit()
      except AssertionError as e:
        return str(e)
      except ValueError as e:
        print(str(e))
      return 'success'
    else:
      return 'fail'
    # success = False
    # if action == 'delete':
    #   success = dataManager.tryRemoveFromDatabase(tableName, key)
    # elif action == 'editRow':
    #   keyFieldName = request.form.get('keyFieldName')
    #   fieldCount = int(request.form.get('fieldCount'))
    #   success = True
    #   for i in range(fieldCount):
    #     fieldName = request.form.get(f'fieldName{i}')
    #     value = request.form.get(f'value{i}')
    #     if not dataManager.tryEditDatabase(tableName, key, fieldName, value):
    #       success = False
    #     if fieldName == keyFieldName:
    #       key = value
    # elif action == 'addRow':
    #   pairs = {}
    #   fieldCount = int(request.form.get('fieldCount'))
    #   for i in range(fieldCount):
    #     fieldName = request.form.get(f'fieldName{i}')
    #     value = request.form.get(f'value{i}')
    #     pairs[fieldName] = value
    #   success = dataManager.tryAddRowToDatabase(tableName, **pairs)
    # if success:
    #   return 'success'
    # else:
    #   return 'fail'
  else:
    return render_template(
      "data.html",
      isLoggedIn = flask_login.current_user.is_authenticated,
      isAdmin = isAdmin(flask_login.current_user),
      airports = models.Airport.query.all(),
      airplanes = models.Airplane.query.all(),
      flights = models.Flight.query.all())

@views.route("generate_data")
@flask_login.login_required
def generate_data():
  if not isAdmin(flask_login.current_user):
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
  if not isAdmin(flask_login.current_user):
    return 'permissionDenied'
  flights = []
  airplanes = []
  airportsFrom = []
  airportsTo = []
  for flight in models.Flight.query.all():
    flights.append(flight)
    airplanes.append(next((airplane for airplane in models.Airplane.query.all() if airplane.id == flight.airplaneId), None))
    airportsFrom.append(next((airport for airport in models.Airport.query.all() if airport.abbreviation == flight.airportFromId), None))
    airportsTo.append(next((airport for airport in models.Airport.query.all() if airport.abbreviation == flight.airportToId), None))
  return render_template("statistics.html",
    isLoggedIn = flask_login.current_user.is_authenticated,
    isAdmin = isAdmin(flask_login.current_user),
    data = zip(flights, airplanes, airportsFrom, airportsTo))

@views.route("arrivalsDepartures", methods=["GET", "POST"])
def arrivalsDepartures():
  flightData = []
  for flight in models.Flight.query.all():
    if flight.isFinished:
      continue
    flightData.append((flight.departureDate.strftime('%Y.%m.%d'),
    flight.departureDate.strftime('%H:%M'), 
    flight.arrivalDate.strftime('%Y.%m.%d'), 
    flight.arrivalDate.strftime('%H:%M'), flight.airportFrom.name, flight.airportTo.name, 
    flight.number))
  return render_template("arrivalsDepartures.html",
    isLoggedIn = flask_login.current_user.is_authenticated,
    isAdmin = isAdmin(flask_login.current_user),
    airports = [model.name for model in models.Airport.query.all()],
    flights = flightData)