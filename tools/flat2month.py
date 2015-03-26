import datetime
import json

def get_month_key(month, year):
    year_offset = year - 2009
    return (year_offset * 12) + month - 1

def get_month_name_from_key(month_key):
    year = month_key / 12
    month = month_key % 12
    monthname = datetime.date(1900, month + 1, 1).strftime('%B')
    return monthname + ' ' + str(year + 2009)

def get_or_insert_key(d, k):
    if k in d:
        v = d[k]
    else:
        v = {}
        d[k] = v
    return v

def normalize_flat_data(months, filename):
    with open(filename) as f:
        contents = f.read()
    data_json = json.loads(contents)

    for e in data_json:
        month = int(e['month'])
        year = int(e['year'])
        precinct = int(e['precinct'])
        month_key = get_month_key(month, year)
        precincts = get_or_insert_key(months, month_key)
        precinct_data = get_or_insert_key(precincts, precinct)
        precinct_data[e['type']] = e['total']

def filter_only_months_with_alldata(months):
    only_months_with_all_data = []
    for month in months:
        has_most_fields = False
        for m in months[month]:
            if len(months[month][m]) >= 4:
                has_most_fields = True
                break

        if has_most_fields:
            month_data = {}
            month_data['month'] = month
            month_data['name'] = get_month_name_from_key(month)
            month_data['precincts'] = months[month]
            only_months_with_all_data.append(month_data)

    month_min = min([m['month'] for m in only_months_with_all_data])
    for month in only_months_with_all_data:
        month['month'] -= month_min

    only_months_with_all_data.sort(lambda a, b: a['month'] > a['month'])
    return only_months_with_all_data

if __name__ == '__main__':
    months = {}
    normalize_flat_data(months, 'jsonresults/visionzero.json')
    normalize_flat_data(months, 'jsonresults/scrape_nycgovcrime.json')
    only_months_with_all_data = filter_only_months_with_alldata(months)
    print(json.dumps(only_months_with_all_data))
