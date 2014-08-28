import logging

from application.checks.model import Check
from application import db


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def save_checks(json_data):
    logger.info("Received POST to check queue. %s" % (json_data))
    check = Check()
    check.title_number = json_data['title_number']
    check.application_type = json_data['application_type']

    db.session.add(check)
    db.session.commit()


def get_check_items():
    return Check.query.order_by(Check.submitted_at).all()
