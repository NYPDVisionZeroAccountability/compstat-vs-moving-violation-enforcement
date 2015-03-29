import json

def get_or_insert_key(d, k, default):
    if k in d:
        v = d[k]
    else:
        v = default
        d[k] = v
    return v

if __name__ == '__main__':
    filename = 'jsonresults/comparison_by_month.json'
    with open(filename) as f:
        contents = f.read()
    months = json.loads(contents)
    precincts = {}
    for month in months:
        for precinct in month['precincts']:
            precinct_data = get_or_insert_key(precincts, precinct['id'], [])
            precinct_data.append({
                'month': month['month'],
                'name': month['name'],
                'data': precinct['data']
            })

    precinct_grouping = []
    for precinct_id in precincts:
        precinct_grouping.append({
            'precinct': precinct_id,
            'months': precincts[precinct_id]
        })

    print(json.dumps(precinct_grouping, sort_keys=True, indent=4, separators=(',', ': ')))
