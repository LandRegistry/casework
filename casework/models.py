from casework import db

class Title_numbers(db.Model):

    __tablename__ = 'title_numbers'

    id = db.Column(db.Integer, primary_key=True)
    title_number = db.Column('title_number', db.String(64))

    def __init__(self, title_number, data):
        self.title_number = title_number

    def __repr__(self):
        return "Title id: %d title number: %s" % (self.id, self.title_number)
