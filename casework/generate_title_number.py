#BRL 2
#Each title needs to be unique
#BRL3
#Each title must have a prefix of TEST immediately followed by numbers in the
# range '1' to '9999' ignoring preceding zeros.

from sqlalchemy import Table, Column, MetaData, Integer
from sqlalchemy.dialects.postgresql import JSON
import os
from casework import db
from casework.models import Title_numbers
from random import randint

class TitleNumber(object):

  def getTitleNumber(self):
    return self.getSequentialTitleNumber()

  def getSequentialTitleNumber(self):
    suffix = self.getNextSuffix()
    return 'TEST' + str(suffix)

  def getNextSuffix(self):
    #get the next number from looking at the title_numbers table.
    #The next line get the last record in the table
    numbers = db.session.query(Title_numbers).order_by(Title_numbers.id.desc()).first()

    if numbers:
      #create the next number and store it
      new_number =  int(numbers.title_number) +  1
      number = Title_numbers(new_number)
      db.session.add(number)
      db.session.commit()
      return new_number
    else:
      #Kick off first title number with a suffix of 1
      number = Title_numbers(1)
      db.session.add(number)
      db.session.commit()
      return 1

# def getRandomTitleNumber(self): #handy for debugging
#   return 'TEST' + str(randint(1,9999))
