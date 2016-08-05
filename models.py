# -*- coding: utf-8 -*-

from tasks import db
from sqlalchemy.dialects.postgresql import JSON

class GooglePlace(db.Model):
  __tablename__ = 'googleplace'

  id = db.Column(db.Integer, primary_key = True)
  place_id = db.Column(db.String())
  data = db.Column(JSON)

  def __init__(self, place_id, data):
    self.place_id = place_id
    self.data = data

  def __repr__(self):
    return '<id {}>'.format(self.id)


class Stamp(db.model):
  __tablename__ = 'stamp'

  id = db.Column(db.Integer, primary_key = True)

