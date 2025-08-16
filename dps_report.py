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
    # Make lists of player accounts and characters
    accounts = [p['account'] for p in d['players']]
    names = [p['name'] for p in d['players']]
    # Make a list of unique mechanic names
    mechanics = list(dict.fromkeys([m['name'] for m in d['mechanics']]))

    # Make an initial dataframe indexed by account with columns of mechanics
    df = pd.DataFrame(index=accounts, columns=mechanics)
    # ensure we can store non-scalars in the mechanics columns
    for m in mechanics:
        df[m] = df[m].astype('object')
    # Add a column for character names
    df['Name'] = names
    for m in d['mechanics']:
        for md in m['mechanicsData']:
            try:
                account = df.index[df['Name'] == md['actor']].tolist()[0]
            except IndexError:
                # this is an NPC actor, make a row for them.
                row = pd.Series(data={m['name']: md['time'],
                                      'Name': md['actor']})
                account = md['actor']
                df.loc[account] = row
            if isinstance(df.at[account, m['name']], float) and \
                    math.isnan(df.at[account, m['name']]):
                # If the cell is a NaN, overwrite it with a list containing
                # the time
                df[m['name']][account] = [md['time'],]
            elif isinstance(df.at[account, m['name']], int):
                # If the cell is an int, make a 2-element list by appending
                # the time
                df[m['name']][account] = [int(df[m['name']][account]),
                                          md['time']]
            else:
                # Append the time
                df.at[account, m['name']].append(md['time'])
    return df
