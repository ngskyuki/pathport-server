# -*- coding: utf-8 -*-

import sys
import requests

# packages for DataBase operation
from flask.ext.sqlalchemy import SQLAlchemy

# packages for formatting result
from flask import jsonify
import operator

# packages for Redis tasks
from rq import Queue
from rq.job import Job
from worker import conn

from app import app

from apikey import APIKEY
from endpoints import *

import json

db = SQLAlchemy(app)
q = Queue(connection = conn)

from models import *

class GooglePlaceConditions:

  def __init__(self, lat, lng, radius = 500, types = 'food', searchtype = 'nearbysearch'):
    self.lat = lat
    self.lng = lng
    self.radius = radius
    self.types = 'food'
    self.baseurl = 'https://maps.googleapis.com/maps/api/place/'
    self.searchtype = 'nearbysearch/'
    self.formattype = 'json'
    self.key = APIKEY

  def get_query(self):
    query = self.baseurl + self.searchtype + self.formattype + '?'
    query += 'location={},{}&radius={}'.format(self.lat, self.lng, self.radius)
    
    if self.types is not '' or self.types is not None:
      query += '&types=' + self.types

    query += '&key={}'.format(self.key)

    return query

# check the record having passed place id
# if there are no place having passed place id then return true
def duplication_check_googleplace(place_id):
  from models import GooglePlace
  count = GooglePlace.query.filter_by(place_id = place_id).count()
  return count == 0

# input: GooglePlace list
# save GooglePlace API result
# output: the count of places saved
def save_googleplace(googleplaces):
  
  counter = 0
  print('Result all count:' + str(len(googleplaces)))

  for gp in googleplaces:
    try:
      from models import GooglePlace
      if duplication_check_googleplace(gp['place_id']):
        googleplace = GooglePlace(
          place_id = gp['place_id'],
          data = gp
        )
        print('Insert')
        db.session.add(googleplace)
      else:
        googleplace = GooglePlace.query.filter_by(place_id = gp['place_id']).first()
        print('Update:')
        googleplace.data = gp

      counter = counter+1

    except:
      print("Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])
      pass

  db.session.commit()
  print("Saved Count:", counter)
  return counter

# call GooglePlace API with passed query : return the raw API result
def get_googleplace(query):
  
  errors = []
  result = {}
  # get the google place informtion
  try:
    print('Use this url:' + query)
    r = requests.get(query)
    return r.json()
  except:
    errors.append(
      "Can not get information"
    )
    return {'error' : errors}
def build_googleplace_query(conditions):
  
  query = ''

  return query

def get_path(conditions):

  errors = []

  # validate conditions
  if conditions.lng is None or conditions.lat is None:
    errors.append(
      "Can not get a location information. Please turn on location."
    )
    return {'error' : errors}

  # building a query
  query = conditions.get_query()

  result_raw = get_googleplace(query)
  
  if 'error' in result_raw:
    return result_raw

  result = result_raw['results']

  # save the google place information
  job = q.enqueue_call(
    func = save_googleplace, args = (result, ), result_ttl = 50
  )

  print('Save GooglePlace Job ID:')
  print(job.id)

  # then return the api-call result
  return result
