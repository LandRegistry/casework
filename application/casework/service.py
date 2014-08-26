import logging

from application import db
from application.casework.model import Casework


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def save_casework(data):
    logger.info("Received POST to casework queue. %s" % (data))
    casework_model = Casework()
    casework_model.title_number = data['title_number']
    casework_model.application_type = data['application_type']

    db.session.add(casework_model)
    db.session.commit()


def get_casework_items():
    return Casework.query.order_by(Casework.submitted_at).all()