import requests
import json

GOOGLE_KEY = 'AIzaSyDW3Wvk6xWLlLI6Bfu29DuDaseX-g18_mo'
TABLE_ID = '02378420399528461352-16143158689603361093'

def get_precinct_data(month, year):
    url = 'https://www.googleapis.com/mapsengine/v1/tables/%s/features/' % TABLE_ID

    params = {
        'key': GOOGLE_KEY,
        'version': 'published',
        'maxResults': 1000,
        'select': 'PCT,TOT',
        'where': 'MO=%s AND YR=%s' % (month, year)
    }

    headers = {
        'referer': 'http://maps.nyc.gov/crime/'
    }

    r = requests.get(url, headers = headers, params = params)
    result = json.loads(r.content)
    features = result['features']

    for f in features:
        yield {
            'precinct': f['properties']['PCT'],
            'total': f['properties']['TOT'],
            'year': year,
            'month': month
        }

if __name__ == '__main__':
    for year in range(2014, 2014):
        for month in range(1, 12):
            precincts = get_precinct_data(month, year)
            for p in precincts:
                print(p)
