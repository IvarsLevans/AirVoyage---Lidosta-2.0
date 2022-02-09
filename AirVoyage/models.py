from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from datetime import datetime
import re

ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
printable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
digits = '0123456789'

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(150))
  surname = db.Column(db.String(150))
  email = db.Column(db.String(150), unique=True)
  psw = db.Column(db.String(150))
  tickets = db.relationship("Ticket")
  def __repr__(self):
    return f'User {self.email}'
  
  @validates('id')
  def validate_id(self, key, id):
    assert re.match('([0-9]+)', id), "Invalid id"
    user = User.query.get(id)
    assert user == None or user == self, "User id must be unique"
    return id
  @validates('name')
  def validate_name(self, key, name):
    assert len(name) >= 1, "Name is too short"
    assert len(name) <= 150, "Name is too long"
    for char in name:
      assert char in ascii_letters, "Invalid name"
    return name
  @validates('surname')
  def validate_surname(self, key, surname):
    if len(surname) < 1:
      raise AssertionError("Surname is too short")
    if len(surname) > 150:
      raise AssertionError("Surname is too long")
    for char in surname:
      if char not in ascii_letters:
        raise AssertionError("Invalid surname")
    return surname
  @validates('email')
  def validate_email(self, key, email):
    assert re.match('([\w.-]+)@([a-z]+)\.([\w]+)', email), "Invalid email"
    user = User.query.filter_by(email = email)
    if user:
      user = user.first()
    assert user == None or user == self, "Email is already used"
    return email
  @validates('psw')
  def validate_psw(self, key, psw):
    assert re.match('.{8,}', psw), "Password must be at least 8 characters"
    return psw


class Airport(db.Model):
  name = db.Column(db.String(150))
  abbreviation = db.Column(db.String(3), primary_key=True)
  address = db.Column(db.String(150))
  airplanes = db.relationship("Airplane")
  incomingFlights = db.relationship("Flight", primaryjoin="and_(Airport.abbreviation==Flight.airportToId, Flight.isFinished==False)", backref='airportTo')
  outgoingFlights = db.relationship("Flight", primaryjoin="and_(Airport.abbreviation==Flight.airportFromId, Flight.isFinished==False)", backref='airportFrom')
  def __repr__(self):
    return f'Airport {self.abbreviation}'
  
  @validates('name')
  def validate_name(self, key, name):
    assert len(name) >= 1, "Name is too short"
    assert len(name) <= 150, "Name is too long"
    assert name[0] in ascii_letters, "Must start with a letter"
    assert name[len(name)-1] in ascii_letters, "Must end with a letter"
    for char in name:
      assert char in ascii_letters + ' .-', "Invalid name"
    return name
  @validates('abbreviation')
  def validate_abbreviation(self, key, abbreviation):
    assert len(abbreviation) == 3, "Must be 3 characters long"
    airplane = Airplane.query.get(abbreviation)
    assert airplane == None or airplane == self, "Abbreviation must be unique"
    for char in abbreviation:
      assert char in ascii_letters, "Invalid abbreviation"
    return abbreviation
  
  @validates('address')
  def validate_address(self, key, address):
    assert len(address) >= 1, "Address is too short"
    assert len(address) <= 150, "Address is too long"
    assert address[0] in ascii_letters, "Must start with a letter"
    assert address[len(address)-1] in ascii_letters, "Must end with a letter"
    for char in address:
      assert char in printable, "Invalid address"
    return address

class Airplane(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  model = db.Column(db.String(150))
  yearOfManufacture = db.Column(db.Integer)
  seats = db.Column(db.Integer)
  airportId = db.Column(db.Integer, db.ForeignKey('airport.abbreviation'));
  flights = db.relationship("Flight", primaryjoin="and_(Airplane.id==Flight.airplaneId, Flight.isFinished==False)", backref='airplane')

  def __repr__(self):
    return f'Airplane {self.id}'

  @validates('id')
  def validate_id(self, key, id):
    assert re.match('([0-9]+)', id), "Invalid id"
    airplane = Airplane.query.get(id)
    assert airplane == None or airplane == self, "Airplane id must be unique"
    return id
  @validates('model')
  def validate_model(self, key, model):
    assert len(model) >= 1, "Model is too short"
    assert len(model) <= 150, "Model is too long"
    for char in model:
      assert char in printable, "Invalid model"
    return model
  @validates('yearOfManufacture')
  def validate_yearOfManufacture(self, key, yearOfManufacture):
    assert len(yearOfManufacture) >= 1, "Year of manufacture is too short"
    assert len(yearOfManufacture) <= 4, "Year of manufacture is too long"
    for char in yearOfManufacture:
      assert char in digits, "Invalid year of manufacture"
    return yearOfManufacture
  @validates('seats')
  def validate_seats(self, key, seats):
    for char in seats:
      assert char in digits, "Invalid seat count"
    assert len(seats) >= 1, "Seat count is too low"
    assert len(seats) <= 5, "Seat count is too high"
    return seats
  @validates('airportId')
  def validate_airportId(self, key, airportId):
    airport = Airport.query.get(airportId)
    assert airport, "Airport does not exist"
    return airportId

class Flight(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  number = db.Column(db.Integer)
  departureDate = db.Column(db.DateTime)
  arrivalDate = db.Column(db.DateTime)
  airportFromId = db.Column(db.String(150), db.ForeignKey('airport.abbreviation'))
  airportToId = db.Column(db.String(150), db.ForeignKey('airport.abbreviation'))
  airplaneId = db.Column(db.Integer, db.ForeignKey('airplane.id'))
  tickets = db.relationship("Ticket", backref='flight')
  isFinished = db.Column(db.Boolean, default=False)
  
  def __repr__(self):
    return f'Flight {self.id}'
  @validates('id')
  def validate_id(self, key, id):
    assert len(id) >= 1, "Invalid id"
    for char in id:
      assert char in digits, "Invalid id"
    flight = Flight.query.get(id)
    assert flight == self or flight == None, "Flight id must be unique"
    return id
  @validates('number')
  def validate_number(self, key, id):
    assert len(id) >= 1, "Invalid number"
    for char in id:
      assert char in digits, "Invalid number"
    return id
  @validates('airportFromId')
  def validate_airportFromId(self, key, airportFromId):
    airport = Airport.query.get(airportFromId)
    assert airport, "Airport does not exist"
    return airportFromId
  @validates('airportToId')
  def validate_airportToId(self, key, airportToId):
    airport = Airport.query.get(airportToId)
    assert airport, "Airport does not exist"
    return airportToId
  @validates('airplaneId')
  def validate_airplaneId(self, key, airplaneId):
    airplane = Airplane.query.get(int(airplaneId))
    assert airplane, "Airplane does not exist"
    return airplaneId
  @validates('isFinished')
  def validate_isFinished(self, key, isFinished):
    if type(isFinished) == bool:
      return isFinished
    elif isFinished.lower() == "true":
      return True
    elif isFinished.lower() == "false":
      return False
    else:
      raise AssertionError("Is finished must be true or false")
  @validates('departureDate')
  def validate_departureDate(self, ket, departureDate):
    if type(departureDate) == datetime:
      return departureDate
    date_ = self.convertToDate(departureDate)
    assert date_, 'Invalid date'
    return date_
  @validates('arrivalDate')
  def calidate_arrivalDate(self, ket, arrivalDate):
    if type(arrivalDate) == datetime:
      return arrivalDate
    date_ = self.convertToDate(arrivalDate)
    assert date_, 'Invalid date'
    return date_

  def convertToDate(self, date):
    numbers = date.split('-')
    try:
      if len(numbers) < 5:
        return datetime.strptime(date, '%Y-%m-%dT%H:%M')
      else:
        return datetime(int(numbers[0]),int(numbers[1]),int(numbers[2]),int(numbers[3]),int(numbers[4]))
    except:
      return None

class Ticket(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  ownerId = db.Column(db.Integer, db.ForeignKey('user.id'))
  flightId = db.Column(db.Integer, db.ForeignKey('flight.id'))
  purchaseDate = db.Column(db.DateTime)
  
  @validates('id')
  def validate_id(self, key, id):
    assert type(id) == int and id >= 0, "Invalid id"
    ticket = Ticket.query.get(id)
    assert ticket == None or ticket == self, "Ticket id must be unique"
    return id

  @validates('ownerId')
  def validate_ownerId(self, key, ownerId):
    assert type(ownerId) == int and ownerId >= 0, "Invalid id"
    owner = User.query.get(int(ownerId))
    assert owner, "Owner does not exist"
    return ownerId
  @validates('flightId')
  def validate_flightId(self, key, flightId):
    for char in flightId:
      assert char in digits, "Invalid flight id"
    flight = Flight.query.get(int(flightId))
    assert flight, "Flight does not exist"
    return flightId
  