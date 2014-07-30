# casework

[![Build Status](https://travis-ci.org/LandRegistry/casework-frontend.svg?branch=master)](https://travis-ci.org/LandRegistry/casework-frontend)

[![Coverage Status](https://img.shields.io/coveralls/LandRegistry/casework-frontend.svg)](https://coveralls.io/r/LandRegistry/casework-frontend)

Basic frontend for title registration

This application requires the following environment variables.

```
SETTINGS
DATABASE_URL
MINT_URL
PROPERTY_FRONTEND_URL
SECRET_KEY
CSRF_ENABLED
```

For local dev these are the settings.

```
export SETTINGS='config.DevelopmentConfig'
export DATABASE_URL='postgresql://localhost/title_number'
export MINT_URL='http://0.0.0.0:8001'
export PROPERTY_FRONTEND_URL='http://0.0.0.0:8002'
export SECRET_KEY='local-dev-not-secret'
export CSRF_ENABLED=True
```

The root url presents a simple registration form. For your benefit and pleasure we have provided a snippet of geojon to help in filling out the form.

Some example valid GEOJson to use on form
```
{
       "type": "Feature",
       "crs": {
         "type": "name",
         "properties": {
           "name": "urn:ogc:def:crs:EPSG:27700"
         }
       },
       "geometry": {
         "type": "Polygon",
         "coordinates":
             [[
     [404439.5558898761,369899.8484076261], [404440.0558898761,369899.8484076261], [404440.0558898761,369900.3484076261], [404439.5558898761,369900.3484076261], [404439.5558898761,369899.8484076261] ]]
     },
     "properties": {
     "Description": "Polygon"
     }
     }
```
