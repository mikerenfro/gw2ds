import argparse
import json 
import urllib.request

import pandas as pd

def read_json_url(u):
    dps_url = f"https://dps.report/getJson?permalink={u}"
    with urllib.request.urlopen(dps_url) as url:
        data = json.load(url)
    return data

def create_mechanics_df(d):
    names = [p['name'] for p in d['players']]
    mechanics = [m['name'] for m in d['mechanics']]
    
    df = pd.DataFrame(index=names, columns=mechanics)
    for m in d['mechanics'][1:]:
        mechanic_actors = [d['actor'] for d in m['mechanicsData']]
        for n in names:
            if n in mechanic_actors:
                df.loc[n][m['name']] = mechanic_actors.count(n)
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='dps.report url')
    args = parser.parse_args()

    data = read_json_url(args.url)
    mechanics_df = create_mechanics_df(data)
    print(mechanics_df)