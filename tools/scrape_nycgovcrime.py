import requests
import json

GOOGLE_KEY = 'AIzaSyDW3Wvk6xWLlLI6Bfu29DuDaseX-g18_mo'
#TABLE_ID = '02378420399528461352-16143158689603361093' total
TABLE_ID = '02378420399528461352-02912990955588156238'

def slugify(word):
    return '-'.join(word.lower().split())

def get_precinct_data(month, year, crime):
    url = 'https://www.googleapis.com/mapsengine/v1/tables/%s/features/' % TABLE_ID

    params = {
        'key': GOOGLE_KEY,
        'version': 'published',
        'maxResults': 1000,
        'select': 'PCT,TOT,CR',
        'where': "MO=%s AND YR=%s AND CR='%s'" % (month, year, crime)
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
            'type': slugify(f['properties']['CR']),
            'year': year,
            'month': month
        }

if __name__ == '__main__':
    for year in range(2014, 2016):
        for month in range(1, 12):
            for crime in ['MURDER', 'FELONY ASSAULT']:
                precincts = get_precinct_data(month, year, crime)
                for p in precincts:
                    print(p)
