import requests
from casework import app

class Mint(object):

    def __init__(self):
        self.api = '%s/titles' % app.config['MINT_URL']

    def post(self, data):
        response = requests.post(self.api, data=data)
        return response
