FROM orchardup/python:2.7
ADD . /code
WORKDIR /code
RUN apt-get install -y git-core
RUN apt-get install -y libpq-dev python-dev
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1
