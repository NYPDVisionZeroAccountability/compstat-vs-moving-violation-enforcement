# https://data.cityofnewyork.us/Public-Safety/Vision-Zero-View-Data/y74e-vkxy
# https://data.cityofnewyork.us/download/y74e-vkxy/application/zip

import shapefile
import json
import requests

# http://www.ariel.com.au/a/python-point-int-poly.html
def point_inside_polygon(x,y,poly):
    n = len(poly)
    inside =False
    if type(poly[0]) != list:
        return False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

def read_district_polygons():
    with open('jsonresults/summary_police_precincts.json') as districts_file:
        districts_content = districts_file.read()
    districts_json = json.loads(districts_content)

    districts = {}
    for f in districts_json['features']:
        precinct = f['properties']['Precinct']
        geometry = f['geometry']['coordinates']
        districts[precinct] = geometry
    return districts

def get_precint_from_lat_lon(lon, lat, precincts):
    for precinct_id in precincts:
        polygons = precincts[precinct_id]
        for polygon in polygons:
            if point_inside_polygon(lon, lat, polygon[0]):
                return precinct_id

if __name__ == '__main__':
    precincts = read_district_polygons()

    with open('jsonresults/injury_all_monthly.json') as visionzero_file:
        visionzero_content = visionzero_file.read()

    visionzero_json = json.loads(visionzero_content)

    data = []
    key_to_type = {
        'PedInjurie': 'pedestrian-injury',
        'BikeInjuri': 'bike-injury',
        'MVOInjurie': 'motor-injury'
    }

    for f in visionzero_json['features']:
        lon, lat = f['geometry']['coordinates']
        precinct = get_precint_from_lat_lon(lon, lat, precincts)

        if precinct:
            props = f['properties']
            for k in key_to_type:
                data.append({
                    'precinct': precinct,
                    'total': props[k],
                    'type': key_to_type[k],
                    'year': props['YR'],
                    'month': props['MN']
                })

    print(json.dumps(data))
