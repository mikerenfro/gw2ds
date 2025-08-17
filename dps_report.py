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
    # Make an initial dataframe indexed by account with columns of mechanics
    df = pd.DataFrame(columns=['mechanic', 'time', 'actor'])

    # ensure we can store non-scalars in the mechanics columns
    for m in d['mechanics']:
        m_name = m['name']
        for md in m['mechanicsData']:
            time = md['time']
            actor = md['actor']
            # print(md)
            df.loc[len(df)] = [m_name, time, actor]

    # print(df)

    return df
