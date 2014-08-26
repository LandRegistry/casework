import datetime

from application import db
from application.frontend.validators import convert_to_bst

class Casework(db.Model):
    __tablename__ = 'casework'

    id = db.Column(db.Integer, primary_key=True)
    title_number = db.Column(db.String(64), nullable=False)
    submitted_at = db.Column(db.DateTime(), default=datetime.datetime.now)
    application_type = db.Column(db.String(50), nullable=False)

    @property
    def with_bst_time(self):
        return convert_to_bst(self.submitted_at)

    @property
    def with_common_app_type(self):
        if self.application_type == 'change-name-marriage':
            return 'change of name'
        else:
            return self.application_type