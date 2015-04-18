import csv
import json
from text2num import text2num
import StringIO

if __name__ == '__main__':
    with open('rawdata/police_budget_fy14.csv') as f:
        police_data = f.read()

    budget_datas = []
    reader = csv.reader(StringIO.StringIO(police_data))
    for precinct, val in reader:
        try:
            precinct = precinct.lower().replace("precinct", "").replace("precint", "").replace("precinc", "").strip()
            precinct_id = text2num(precinct)
            for m in range(1, 13):
                budget_datas.append({
                    "month": m,
                    "precinct": precinct_id,
                    "total": int(val) / 12,
                    "type": "budget",
                    "year": 2014
                })
        except:
            # TODO: for now, skip everything else, we are skipping about 7
            pass

    print(json.dumps(budget_datas))
