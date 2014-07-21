#BRL 2
#Each title needs to be unique
#BRL3
#Each title must have a prefix of TEST immediately followed by numbers in the
# range '1' to '9999' ignoring preceding zeros.
#No method to prevent title reuse so far.
from random import randint

class TitleNumber(object):

  instance_suffix = 0

  def getRandomTitleNumber(self):
    return 'TEST' + str(randint(1,9999))

  def getSequentialTitleNumber(self):
    suffix = self.getNextSuffix()
    return 'TEST' + str(suffix)

  def getNextSuffix(self):
    #get the next number from looking at a file or database.
    return self.instance_suffix

  def getTitleNumber(self):
    return self.getSequentialTitleNumber()


# rtn = RandomTitleNumber()
# print rtn.getRandomTitleNumber()
