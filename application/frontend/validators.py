#from shapely.geometry import mapping, shape
import simplejson
from datetime import date

from pytz import timezone
from wtforms.validators import ValidationError
from application import app
import logging


class ValidateDateNotInFuture(object):
    def __call__(self, form, date_field):
        if date_field.data > date.today():
            raise ValidationError('Date cannot be in the future')

def convert_to_bst(dt):
    utc = timezone('UTC').localize(dt)
    bst = timezone('Europe/London').localize(dt)
    return bst + (utc - bst)


# class ValidateEasementWithinExtent(object):
#     def __init__(self):
#         self.message = "The easement extent must exist within the charge extent"
#
#     def __call__(self, form, extent_geo):
#       if(form.easements):
#           extent_dict = simplejson.loads(extent_geo.data)
#           easement_dict = simplejson.loads(form.easements[0].easement_geometry.data)
#           app.logger.info(extent_dict.get('geometry'))
#           app.logger.info(easement_dict.get('geometry'))
#
#           extent = shape(extent_dict.get('geometry'))
#           easement = shape(easement_dict.get('geometry'))
#
#           if not(extent.contains(easement)):
#             raise ValidationError('Easement geometry must exist within the extent.')
