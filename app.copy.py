# -*- coding: utf-8 -*-

import os
import requests
import json
import operator

# packages for flask application running
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

# packages for flask-RESTFUL
from flask_restful import Resource, Api

# packages for redis
from rq import Queue
from rq.job import Job
from worker import conn

# packages for format result
from flask import jsonify

# register this module as Flask application
app = Flask(__nam__)

# some configurations
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# load the database
db = SQLAlchemy(app)

q = Queue(connection = conn)

from models import *

api = Api(app)

class Test(Resource):
  def get(self):
    return {'hello' : 'world'}


def get_path():
  
  errors = []

  url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=35.5331548,139.6936981&radius=500&types=food&key=' + 'apikey'

  if url is None:
    errors.append(
      "Unable to get paths."
    )
    return {'error' : errors}

  try:
    r = requests.get(url)
  except:
    errors.append(
      "Can not get information."
    )
    return {'erorr' : errors}

  # get the api result
  result_json = json.loads(r.text)

  #TODO: make result formatted

  # save the result
  try:
    #TODO: need some duplication check
    # if not duplicated, then save it.
    from models import Path
    path = Path(
      data = result_json
    )
    db.session.add(path)
    db.session.commit()
    return path.id
  except:
    print('database error occured.')
    errors.append("Unable to add item to database.")
    return {'error' : errors}

@app.route('/', methods = ['GET', 'POST']
def index():
  results = {}
  return render_template('index.html', result = results)


