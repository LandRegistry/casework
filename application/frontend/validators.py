# -*- coding: utf-8 -*-
from shapely.geometry import mapping, shape
import simplejson
from datetime import date

from pytz import timezone
from wtforms.validators import ValidationError
from application import app
import logging


class ValidateDateNotInFuture(object):
    def __init__(self):
        self.message = "The date must not be in the future"

    def __call__(self, form, date_field):
        if date_field.data > date.today():
            raise ValidationError('Date cannot be in the future')

class ValidateEasementWithinExtent(object):
    def __init__(self):
        self.message = "The easement extent must exist within the charge extent"

    def __call__(self, form, extent_geo):
      extent_json = simplejson.dumps(extent_geo.data)
      app.logger.info(extent_geo.data)
      extent = shape(simplejson.loads(extent_geo.data))
      #easement = shape(simplejson.loads(form.easements[0].easement_geometry.data))
      if (extent_geo.data == form.easements[0].easement_geometry.data):
        raise ValidationError('Easement geometry must exist within the extent.')

      #This is what shapely wants.  
      # {
      #     "type": "Polygon",
      #     "coordinates": [
      #         [
      #             [
      #                 404439.5558898761,
      #                 369899.8484076261
      #             ],
      #             [
      #                 404440.0558898761,
      #                 369899.8484076261
      #             ],
      #             [
      #                 404440.0558898761,
      #                 369900.3484076261
      #             ],
      #             [
      #                 404439.5558898761,
      #                 369900.3484076261
      #             ],
      #             [
      #                 404439.5558898761,
      #                 369899.8484076261
      #             ]
      #         ]
      #     ]
      # }



def convert_to_bst(dt):
    utc = timezone('UTC').localize(dt)
    bst = timezone('Europe/London').localize(dt)
    return bst + (utc - bst)
