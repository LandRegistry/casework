valid_geo_json = {
    "type": "Feature",

    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:EPSG:27700"
        }
    },

    "geometry": {
        "type": "Polygon", "coordinates": [
        [
            [530857.01, 181500.00],
            [530857.00, 181500.00],
            [530857.00, 181500.00],
            [530857.00, 181500.00],
            [530857.01, 181500.00]
        ]
    ]},

    "properties": {

    }
}

invalid_geo_point = {
    "type": "Feature",

    "geometry": {
        "type": "Point",
        "coordinates": [125.6, 10.1]
    },

    "properties": {
        "name": "Dinagat Islands"
    }
}