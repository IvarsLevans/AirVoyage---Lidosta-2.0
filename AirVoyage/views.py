from flask import Blueprint, render_template, redirect, request
from . import db
from . import models
import flask_login
import re

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
    if request.form.get('action') == 'edit':
      if request.form.get('value') == '':
        return ''
      elif not re.search('[a-zA-Z0-9]', request.form.get('value')):
        return ''
      if request.form.get('table') == 'airports':
        print("h")
        try:
          airport = models.Airport.query.filter_by(abbreviation = request.form.get('key')).first()
          try:
            setattr(airport, request.form.get('field'), request.form.get('value'))
            db.session.commit()
            print(getattr(airport, request.form.get('field')))
            return 'success'
          except:
            print(getattr(airport, request.form.get('field')))
            return getattr(airport, request.form.get('field'))
          return ''
        except:
          pass
        return ''
      elif request.form.get('table') == 'airplanes':
        try:
          airplane = models.Airplane.query.filter_by(id = request.form.get('key')).first()
          try:
            setattr(airplane, request.form.get('field'), request.form.get('value'))
            db.session.commit()
            return 'success'
          except:
            return getattr(airplane, request.form.get('field'))
          return ''
        except:
          pass
        return ''
      return ''
    elif request.form.get('action') == 'new':
      if request.form.get('value') == '':
        return ''
      elif not re.search('[a-zA-Z0-9]', request.form.get('value')):
        return ''
      if request.form.get('table') == 'airports':
        try:
          db.session.add(models.Airport(abbreviation = request.form.get('value')))
          db.session.commit()
          return 'success'
        except:
          pass
      elif request.form.get('table') == 'airplanes':
        try:
          db.session.add(models.Airplane(id = request.form.get('value')))
          db.session.commit()
          return 'success'
        except:
          print('error')
          pass
      return ''
    elif request.form.get('action') == 'getData':
      return str(models.Airport.query.all());
    elif request.form.get('action') == 'delete':
      airport = models.Airport.query.filter_by(abbreviation=request.form.get('key')).first()
      if airport is None:
        return 'failed'
      else:
        db.session.delete(airport)
        db.session.commit()
        return 'successful'
  else:
    return render_template(
      "data.html",
      isLoggedIn = flask_login.current_user.is_authenticated,
      airports = models.Airport.query.all(),
      airplanes = models.Airplane.query.all())

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