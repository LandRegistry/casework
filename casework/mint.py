import requests


class Mint(object):

    def __init__(self):
        self.api = 'http://0.0.0.0:8001/titles'

    def post(self, data):
        response = requests.post(self.api, data=data)
        return response
