import argparse

import dps_report as dr

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='dps.report url')
    args = parser.parse_args()

    data = dr.read_json_url(args.url)
    mechanics_df = dr.create_mechanics_df(data)
    print("Overall dataframe")
    # print(mechanics_df['Exposed'])

    print("\nWho died when?")
    death_df = mechanics_df.loc[mechanics_df['mechanic'] == 'Dead'].sort_values('time')
    print(death_df)

    print("\nWhat about exposures?")
    exposed_df = mechanics_df.loc[mechanics_df['mechanic'] == 'Exposed'].sort_values('time')
    print(exposed_df)
