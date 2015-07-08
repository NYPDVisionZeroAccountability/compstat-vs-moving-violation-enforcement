import json

if __name__ == '__main__':
    filename = 'jsonresults/comparison_by_month.json'
    with open(filename) as f:
        contents = f.read()
    months = json.loads(contents)
    rows = []
    for month in months:
        for i, precinct in enumerate(month['precincts']):
            row = {
                'id': i,
                'precinct': precinct['id'],
                'month': month['month'],
                'name': month['name'],
            }

            data = precinct['data']
            for d in data:
                row[d['type']] = d['val']

            rows.append(row)

    print(json.dumps(rows, sort_keys=True, indent=4, separators=(',', ': ')))
