# casework

[![Build Status](https://travis-ci.org/LandRegistry/casework-frontend.svg?branch=master)](https://travis-ci.org/LandRegistry/casework-frontend)

[![Coverage Status](https://img.shields.io/coveralls/LandRegistry/casework-frontend.svg)](https://coveralls.io/r/LandRegistry/casework-frontend)

This app was created using the scaffolder at https://github.com/LandRegistry/flask-example-scaffold

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
