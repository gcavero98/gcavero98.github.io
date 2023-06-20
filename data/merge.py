import random

import numpy as np
import os
from pathlib import Path

import pandas as pd

months = range(1, 12 + 1)
years = range(2019, 2022 + 1)

print(list(months))
print(list(years))

path = Path('.') / 'bicing'
files = list(map(lambda x: x.resolve().as_uri(), path.glob('*.csv')))

files = np.sort(files)

folders_per_year = [
    path / str(year) for year in years
]

for folder in folders_per_year:
    folder.mkdir(exist_ok=True)

for file in files:
    df = pd.read_csv(file)
    gdf = df.groupby(['year'], as_index=False).agg({'station_id': 'count'})
    year = gdf.sort_values('station_id', ascending=False).loc[0].year
    df.drop(columns=df.columns[0]).to_csv(path / str(year) / (str(int(random.random()*1_000_000_000)) + '.csv'))
