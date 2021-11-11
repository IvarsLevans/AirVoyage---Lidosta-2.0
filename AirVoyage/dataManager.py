import re
from . import models
from . import db
import datetime

booleanFields = ['isFinished']
dateFields = ['departureDate', 'arrivalDate']
def tryEditDatabase(table, key, fieldName, value):
  if fieldName not in booleanFields:
    if not checkValue(value):
      return False
  modelType = getModelType(table)
  if modelType is None:
    return False
  row = modelType.query.get(key)
  if row is None:
    return False
  try:
    print(row, fieldName, value)
    if fieldName in booleanFields:
      if value == 'true':
        setattr(row, fieldName, True)
      elif value == 'false':
        setattr(row, fieldName, False)
      else:
        return False
    elif fieldName in dateFields:
      numbers = value.split('-')
      setattr(row, fieldName, datetime.datetime(int(numbers[0]),int(numbers[1]),int(numbers[2]),int(numbers[3]),int(numbers[4])))
    else:
      setattr(row, fieldName, value)
    db.session.commit()
  except:
    return False
  return True

def tryAddToDatabase(table, value):
  if not checkValue(value):
    return False
  try:
    if table == 'airports':
      db.session.add(models.Airport(abbreviation = value))
    elif table == 'airplanes':
      db.session.add(models.Airplane(id = value))
    elif table == 'flights':
      db.session.add(models.Flight(id = value))
    else:
      return False
    db.session.commit()
  except:
    return False
  return True

def tryRemoveFromDatabase(table, key):
  print(table)
  modelType = getModelType(table)
  print(modelType)
  if modelType is None:
    return False
  row = modelType.query.get(key)
  if row is None:
    return False
  try:
    db.session.delete(row)
    db.session.commit()
  except:
    return False
  return True

def getModelType(tableName):
  modelType = None
  if tableName == 'airports':
    modelType = models.Airport
  elif tableName == 'airplanes':
    modelType = models.Airplane
  elif tableName == 'flights':
    modelType = models.Flight
  return modelType

def checkValue(value):
  if value == '':
    return False
  elif not re.search('[a-zA-Z0-9]', value):
    return False
  else:
    return True

def isAdmin(user):
  admins = ['admin@admin.admin']
  if user.is_authenticated and user.email in admins:
    return True
  else:
    return False
# if request.form.get('action') == 'edit':
#       if request.form.get('value') == '':
#         return ''
#       elif not re.search('[a-zA-Z0-9]', request.form.get('value')):
#         return ''
#       if request.form.get('table') == 'airports':
#         print("h")
#         try:
#           airport = models.Airport.query.filter_by(abbreviation = request.form.get('key')).first()
#           try:
#             setattr(airport, request.form.get('field'), request.form.get('value'))
#             db.session.commit()
#             print(getattr(airport, request.form.get('field')))
#             return 'success'
#           except:
#             print(getattr(airport, request.form.get('field')))
#             return getattr(airport, request.form.get('field'))
#           return ''
#         except:
#           pass
#         return ''
#       elif request.form.get('table') == 'airplanes':
#         try:
#           airplane = models.Airplane.query.filter_by(id = request.form.get('key')).first()
#           try:
#             setattr(airplane, request.form.get('field'), request.form.get('value'))
#             db.session.commit()
#             return 'success'
#           except:
#             return getattr(airplane, request.form.get('field'))
#           return ''
#         except:
#           pass
#         return ''
#       return ''
#     elif request.form.get('action') == 'new':
#       if request.form.get('value') == '':
#         return ''
#       elif not re.search('[a-zA-Z0-9]', request.form.get('value')):
#         return ''
#       if request.form.get('table') == 'airports':
#         try:
#           db.session.add(models.Airport(abbreviation = request.form.get('value')))
#           db.session.commit()
#           return 'success'
#         except:
#           pass
#       elif request.form.get('table') == 'airplanes':
#         try:
#           db.session.add(models.Airplane(id = request.form.get('value')))
#           db.session.commit()
#           return 'success'
#         except:
#           print('error')
#           pass
#       return ''
#     elif request.form.get('action') == 'getData':
#       return str(models.Airport.query.all());
#     elif request.form.get('action') == 'delete':
#       airport = models.Airport.query.filter_by(abbreviation=request.form.get('key')).first()
#       if airport is None:
#         return 'failed'
#       else:
#         db.session.delete(airport)
#         db.session.commit()
#         return 'successful'