from pathlib import Path
from typing import List

import numpy as np
import pandas as pd


def load_per_years(folder: Path, years: List[int | str], pandas_kwargs=None):
    assert folder.exists(), "Please introduce a valid folder"
    pandas_kwargs = pandas_kwargs or {}

    data_folders = [folder / f'{y}' for y in years]

    return pd.concat([pd.read_csv(file, **pandas_kwargs) for data_folder in data_folders for file in
                      data_folder.glob('*/*.csv')]).drop_duplicates()


def postprocess(data):
    print("Post-processing...")
    data = data.copy()  # make sure that this function does not modify the orignal object

    data_ = data.assign(
        datetime=lambda x: pd.to_datetime(x.datetime),
        percentage_docks_available=lambda x: x.num_docks_available / (x.num_docks_available + x.num_bikes_available),
    ).drop(columns=['num_docks_available', 'num_bikes_available'])

    print("Filtering invalid...")
    data_ = data_.query(f'percentage_docks_available >= 0').query(f'percentage_docks_available <= 1')

    print("Adding features...")
    data_ = data_.sort_values(['station_id', 'datetime']).assign(
        day_of_week=lambda x: x.datetime.dt.day_of_week,
        month_name=lambda x: x.datetime.dt.month_name,
        day_name=lambda x: x.datetime.dt.day_name,
        is_weekend=lambda x: x.day_of_week >= 5,
        is_night=lambda x: np.bitwise_or(x.hour >= 20, x.hour <= 7),
        is_work_morning=lambda x: np.bitwise_and(x.hour >= 6, x.hour <= 10) & np.bitwise_not(x.is_weekend),
        is_summer=lambda x: x.month.between(6, 8),
        ctx_1=lambda x: x.percentage_docks_available.shift(1),
        ctx_2=lambda x: x.percentage_docks_available.shift(2),
        ctx_3=lambda x: x.percentage_docks_available.shift(3),
        ctx_4=lambda x: x.percentage_docks_available.shift(4),
        station_id_aux=lambda x: x.station_id.shift(4),
    )

    print("Quering invalid...")
    data_ = data_ \
        .query('not ctx_1.isnull()') \
        .query('not ctx_2.isnull()') \
        .query('not ctx_3.isnull()') \
        .query('not ctx_4.isnull()') \
        .query('station_id == station_id_aux') \
        .drop(columns=['station_id_aux']) \
        .query('not percentage_docks_available.isnull()')

    return data_


def add_geo_data(geo_csv_path: Path, data: pd.DataFrame):
    assert geo_csv_path.exists()
    print("Adding geo data...")

    data = data.copy()  # make sure that this function does not modify the orignal object

    station_info = pd.read_csv(geo_csv_path)
    data = pd.merge(
        left=data, right=station_info[['station_id', 'lat', 'lon', 'altitude', 'post_code']],
        on=['station_id']
    )

    return data


def add_climate_data(climate_csv_path: Path, data: pd.DataFrame):
    assert climate_csv_path.exists()
    print("Adding climate data...")

    data = data.copy()  # make sure that this function does not modify the orignal object

    df_climate_ = pd.read_csv(climate_csv_path, parse_dates=['time'])

    df_climate = df_climate_.assign(
        year=df_climate_.time.dt.year,
        month=df_climate_.time.dt.month,
        day=df_climate_.time.dt.day,
        hour=df_climate_.time.dt.hour
    )

    data = pd.merge(
        left=data,
        right=df_climate.drop(columns=['time']),
        on=['hour', 'day', 'month', 'year']
    )

    return data


import datetime


def spanish_date_to_datetime(sp_date: str):
    y, m, d = sp_date.split('/')[::-1]
    return datetime.date(int(y), int(m), int(d))


def get_festivos(folder):
    info_festivos = pd.concat([pd.read_csv(file, index_col=0) for file in folder.glob('*.csv')])
    s = pd.Series(name='date'   )
    for i, festivo in info_festivos.iterrows():
        start_date, end_date = spanish_date_to_datetime(festivo.DataInici), spanish_date_to_datetime(festivo.DataFi)

        dr = pd.date_range(start_date, end_date, freq='d').to_series()
        s = pd.concat([s, dr], ignore_index=True)

    return pd.DataFrame(s.sort_values()).assign(
        year=s.dt.year,
        month=s.dt.month,
        day=s.dt.day,
        festivo=True
    )


def add_festivos(festivos_folder, data):
    print("Adding festivos...")
    dias_festivos = get_festivos(festivos_folder)
    data = pd.merge(
        left=data.copy(),
        right=dias_festivos[['festivo', 'day', 'month', 'year']],
        how='left',
        on=['day', 'month', 'year']
    )
    return data

