import unittest

from application import db
from application.casework.model import Casework


class CaseworkModelTest(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def casework_model_with_common_app_type_returns_right_label(self):
        casework = Casework()
        casework.title_number = 'title_number'
        casework.application_type = 'change-name-marriage'

        db.session.add(casework)

        result = Casework.query.all()
        assert result[0].title_number == casework.title_number






