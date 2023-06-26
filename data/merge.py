import datetime
import random

from tqdm import tqdm

import numpy as np
import os
from pathlib import Path

import pandas as pd

months = range(1, 12 + 1)
years = range(2019, 2022 + 1)

print(list(months))
print(list(years))

source_path = Path('./data/csv')
destination_path = Path('./data/bicing')

files = list(map(lambda x: x.resolve().as_uri(), source_path.glob('*.csv')))
files = np.sort(files)

folders_per_year = [
    destination_path / mode / str(year) / str(month) for mode in ['raw', 'truncated'] for year in years for month in
    months
]

for folder in folders_per_year:
    folder.mkdir(exist_ok=True, parents=True)

COLUMNS = [
    'station_id',
    'datetime',
    'year',
    'month',
    'day',
    'hour',
    'num_bikes_available',
    'num_docks_available'
]


def preprocess(data):
    data = data[~data.last_updated.isna()]

    data = data.assign(
        datetime_raw=lambda x: x.last_updated.apply(datetime.datetime.fromtimestamp),
        datetime=lambda x: x.datetime_raw.dt.floor('h'),
        year=lambda x: x.datetime.dt.year,
        month=lambda x: x.datetime.dt.month,
        day=lambda x: x.datetime.dt.day,
        hour=lambda x: x.datetime.dt.hour
    )

    data = data[data.status == 'IN_SERVICE']

    gdata = data.groupby(
        ['station_id', 'datetime', 'year', 'month', 'day', 'hour'], as_index=False
    ).agg({
        'num_bikes_available': 'mean',
        'num_docks_available': 'mean'
    })

    return data, gdata


if __name__ == '__main__':
    for file in tqdm(files[-6:]):
        df = pd.read_csv(file)

        df_, gdf_ = preprocess(df)

        # split df in years
        years_and_months = gdf_.groupby(['year', 'month'], as_index=False).agg({'station_id': 'count'})

        for ii, row in years_and_months.iterrows():
            y, m = row.year, row.month
            if int(y) == 2023:
                continue
            print(f'Saving: {y}-{m}')
            df_[COLUMNS] \
                .query(f'month == {m} and year == {y}') \
                .sort_values(['datetime', 'station_id']) \
                .to_csv(destination_path / 'raw' / str(y) / str(m) / f'{int(random.randint(0 ,1_000_000_000))}.csv')
            gdf_[COLUMNS] \
                .query(f'month == {m} and year == {y}') \
                .sort_values(['datetime', 'station_id']) \
                .to_csv(
                destination_path / 'truncated' / str(y) / str(m) / f'{int(random.randint(0 ,1_000_000_000))}.csv')
