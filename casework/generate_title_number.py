#BRL 2
#Each title needs to be unique
#BRL3
#Each title must have a prefix of TEST immediately followed by numbers in the
# range '1' to '9999' ignoring preceding zeros.
#No method to prevent title reuse so far.
from random import randint

class RandomTitleNumber(object):
  def getRandomTitleNumber(self):
    return 'TEST' + str(randint(1,9999))


# rtn = RandomTitleNumber()
# print rtn.getRandomTitleNumber()
