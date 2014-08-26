from datetime import datetime


def generate_title_number():
    return 'TEST%d' % int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)