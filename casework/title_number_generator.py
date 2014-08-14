import random
from datetime import datetime


def TimestampMillisec64():
    return int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)


def generate_title_number():
    return 'TEST%d' % TimestampMillisec64()