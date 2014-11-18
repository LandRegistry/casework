# casework

[![Build Status](https://travis-ci.org/LandRegistry/casework-frontend.svg?branch=master)](https://travis-ci.org/LandRegistry/casework-frontend)

[![Coverage Status](https://img.shields.io/coveralls/LandRegistry/casework-frontend.svg)](https://coveralls.io/r/LandRegistry/casework-frontend)

Basic frontend for casework.  This application can:

 1) Display name change requests from the Service Frontend
 2) Display name change requests from the Service Frontend that need further checking.


This application depends on the following services:

```
Mint - https://github.com/LandRegistry/mint
Property-Frontend - https://github.com/LandRegistry/property-frontend
Cases - https://github.com/LandRegistry/cases
```

The application also depends on the following:

```
Postgres
Python modules specified in requirements.txt - https://github.com/LandRegistry/casework-frontend/blob/master/requirements.txt
```

###Using the development environment

```
You can use the development environment created for the alpha: https://github.com/LandRegistry/development-environment
```

###Running the application manually:

```
Install the python modules within requirements.txt.  Recommend doing this in a virtual environment.  If pip is
installed, you can type "pip install -r requirements.txt"

You can manually run the app by typing ./run_dev.sh in the terminal.  This will start the application on port 5000.
The script exports the environment variables needed to run the application.  However, to login and use the application
you will need to create the database for the application, then restart the server.

```

###Create the database and tables

```
run the script to create the database by typing ./db/create_database.sh
run the script to create the tables by typing ./upgrade_db.sh

```

Create Users to login to the the application, by adding them to the user database.

Locally:
```
run ./create_user.sh     This includes the necessary exports and creates a user with the line below:

python manage.py create_user --email=testuser@mail.com --password=password --active=t

```

On Heroku:
```
heroku run python manage.py create_user --email=testuser@mail.com --password=password --active=t --app lr-casework-frontend
```

The fixtures application can also be used to create users relationships to titles. https://github.com/LandRegistry/fixtures

