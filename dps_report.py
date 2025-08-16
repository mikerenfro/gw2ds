import json
import math
import urllib.request

import pandas as pd


def read_json_url(u):
    dps_url = f"https://dps.report/getJson?permalink={u}"
    with urllib.request.urlopen(dps_url) as url:
        data = json.load(url)
    return data


def create_mechanics_df(d):
    accounts = [p['account'] for p in d['players']]
    names = [p['name'] for p in d['players']]
    mechanics = [m['name'] for m in d['mechanics']]

    df = pd.DataFrame(index=accounts, columns=mechanics)
    for m in mechanics:
        df[m] = df[m].astype('object')
    df['Name'] = names
    for m in d['mechanics']:
        for md in m['mechanicsData']:
            account = df.index[df['Name'] == md['actor']].tolist()[0]
            if isinstance(df.at[account, m['name']], float) and \
                    math.isnan(df.at[account, m['name']]):
                df.at[account, m['name']] = md['time']
            elif isinstance(df.at[account, m['name']], int):
                df.at[account, m['name']] = [df.at[account, m['name']],
                                             md['time']]
            else:
                df.at[account, m['name']].append(md['time'])
    return df
