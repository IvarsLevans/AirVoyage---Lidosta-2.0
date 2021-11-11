from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(150))
  surname = db.Column(db.String(150))
  email = db.Column(db.String(150), unique=True)
  psw = db.Column(db.String(150))
  tickets = db.relationship("Ticket")
  def __repr__(self):
    return f'User {self.email}'

class Airport(db.Model):
  name = db.Column(db.String(150))
  abbreviation = db.Column(db.String(3), primary_key=True)
  address = db.Column(db.String(150))
  airplanes = db.relationship("Airplane")
  def __repr__(self):
    return f'Airport {self.abbreviation}'

class Airplane(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  model = db.Column(db.String(150))
  yearOfManufacture = db.Column(db.Integer)
  seats = db.Column(db.Integer)
  airportId = db.Column(db.Integer, db.ForeignKey('airport.abbreviation'));
  flights = db.relationship("Flight", primaryjoin="and_(Airplane.id==Flight.airplaneId, Flight.isFinished==False)", backref='airplane')
  def __repr__(self):
    return f'Airplane {self.id}'

class Flight(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  number = db.Column(db.Integer)
  departureDate = db.Column(db.DateTime)
  arrivalDate = db.Column(db.DateTime)
  airportFrom = db.Column(db.String(150))
  airportTo = db.Column(db.String(150))
  airplaneId = db.Column(db.Integer, db.ForeignKey('airplane.id'))
  tickets = db.relationship("Ticket", backref='flight')
  isFinished = db.Column(db.Boolean, default=False)
  def __repr__(self):
    return f'Flight {self.id}'

class Ticket(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  ownerId = db.Column(db.Integer, db.ForeignKey('user.id'))
  flightId = db.Column(db.Integer, db.ForeignKey('flight.id'))
  