from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150), unique=True)
  psw = db.Column(db.String(150))
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
  flights = db.relationship("Flight")
  def __repr__(self):
    return f'Airplane {self.id}'
  def __unicode__(self):
    return "[%s(%s)]" % (self.__class__.__name__, ', '.join('%s=%s' % (k, self.__dict__[k]) for k in sorted(self.__dict__) if '_sa_' != k[:4]))

class Flight(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  number = db.Column(db.Integer)
  departureDate = db.Column(db.Date)
  arrivalDate = db.Column(db.Date)
  airportFrom = db.Column(db.String(150))
  airportTo = db.Column(db.String(150))
  airplaneId = db.Column(db.Integer, db.ForeignKey('airplane.id'))
  def __repr__(self):
    return f'Flight {self.id}'