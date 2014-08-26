import logging
import requests
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

def post_to_mint(json_data, url):
    logger.info(json_data)
    title_url = '%s/%s' % (url, json_data['title_number'])
    headers = {'content-type': 'application/json'}
    logger.info("Sending data %s to the mint at %s" % (json_data, title_url))
    try:
        response = requests.post(title_url, data=json.dumps(json_data), headers=headers)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Could not create title number %s: Error %s" % (title_url, e))
        raise RuntimeError