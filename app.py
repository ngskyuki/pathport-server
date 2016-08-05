# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

from tasks import *

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

class PrintPath(Resource):
  def get(self):
    return get_sample()

class GetPath(Resource):
  def get(self, lat, lng):
    conditions = GooglePlaceConditions(lat, lng)
    return get_path(conditions)


#api.add_resource(PrintPath, '/')
api.add_resource(GetPath, '/path/<string:lat>/<string:lng>')

if __name__ == '__main__':
  app.run(debug = True)
