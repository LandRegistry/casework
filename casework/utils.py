import re

def validate_ogc_urn(crs):
    """
    Method that validates a OGC (Open Geospatial Consortium) CRS (Co-ordinate
    Reference System) URN (Unique Reference Name). Must be an EPSG (European Petroleum
    Survey Group) code, e.g. EPSG:27700 for British National Grid.
    http://www.opengeospatial.org/ogcUrnPolicy
    """

    pattern = 'urn:ogc:def:crs:EPSG:\d{4,5}'
    return re.match(pattern, crs) != None
