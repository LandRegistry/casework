import requests
from casework import app

class Mint(object):

    def __init__(self):
        self.api = '%s/title' % app.config['MINT_URL']

    def post(self, title_number, json_data):
        title_url = '%s/%s' % (self.api, title_number)
        headers = {'content-type': 'application/json'}
        app.logger.info("Sending data %s to the mint at %s" % (json_data, title_url))
        response = requests.post(title_url, data = json_data, headers=headers)
        return response
