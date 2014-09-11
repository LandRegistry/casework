import requests
import logging
from flask import current_app
from requests.auth import HTTPBasicAuth


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

def get_cases(queue):
    url = current_app.config['CASES_URL'] + "/cases/queue/" + queue
    logging.info("GET_CASES for url: %s" % url)
    response = requests.get(url)

    logging.info("JSON: %s" % response.json())
    return response.json()

def complete_case(case_id):
    url = current_app.config['CASES_URL'] + "/cases/complete/"+ case_id
    logging.info("POST %s" % url)


    return requests.put(url)