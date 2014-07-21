import requests
from casework import app

class Mint(object):

    def __init__(self):
        self.api = '%s/titles' % app.config['MINT_URL']

    def post(self, title_number, json_data):
        title_url = '%s/%s' % (self.api, title_number)
        headers = {'content-type': 'application/json'}
        app.logger.info("Sending data %s to the mint at %s" % (json_data, title_url))
        try:
            response = requests.post(title_url, data = json_data, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            app.logger.error("Could not create title number %s: Error %s" % (title_url, e))
            raise RuntimeError

    def __repr__(self):
        return self.api
