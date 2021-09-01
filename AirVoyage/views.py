from flask import Blueprint, render_template, request, flash, jsonify

views = Blueprint("views", __name__)

@views.route('/')
def index():
  return render_template("index.html")

@views.route('templates/d&aAirport1.html')
def Airport1():
  return render_template("d&aAirport1.html")

@views.route('templates/d&aAirport2.html')
def Airport2():
  return render_template("d&aAirport2.html")

@views.route('templates/d&aAirport3.html')
def Airport3():
  return render_template("d&aAirport3.html")

@views.route('templates/d&aAirport4.html')
def Airport4():
  return render_template("d&aAirport4.html")
