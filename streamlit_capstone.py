from pathlib import Path
from backend import loader

import streamlit as st
import pydeck as pdk

import pandas as pd
import numpy as np
import seaborn as sns

st.set_page_config(layout='wide')
import calendar
import matplotlib.pyplot as plt

MAX_ROWS = 100_000
Y_COLUMN = 'percentage_docks_available'


@st.cache_data
def init_connection():
    print("Initializing connection...")
    folder_with_data = Path.cwd() / 'data' / 'bicing' / 'truncated'
    df_raw = loader.load_per_years(
        folder_with_data,
        [2021, 2022],
        pandas_kwargs={'index_col': 0}
    )
    geo_csv_path = Path.cwd() / 'data' / 'bicing_info.csv'
    climate_csv_path = Path.cwd() / 'data' / 'clima.csv'

    df_extended = loader.add_festivos(
        Path.cwd() / 'data' / 'festivos',
        loader.add_climate_data(
            climate_csv_path,
            loader.add_geo_data(
                geo_csv_path,
                loader.postprocess(df_raw)
            )
        )
    )

    print("Loaded!")
    return df_extended.sample(n=MAX_ROWS)


df = init_connection()
print(df.head())

col1, col2, col3 = st.columns(3)

df = df.assign(
    month_name=lambda x: x.datetime.dt.month_name,
    day_name=lambda x: x.datetime.dt.day_name,
)
unique_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December', ]

selected_day = col1.selectbox('Day of the week', options=unique_days)
selected_month = col2.selectbox('Month', options=months)
selected_hour = col3.slider('Select an hour slice', min_value=0, max_value=24, step=1)


def filter_df(data, day, month, hour):
    return data \
        .query(f'day_of_week == "{day}"') \
        .query(f'month_name == "{month}"') \
        .query(f'hour == {hour}')


df_density = filter_df(df, selected_day, selected_month, selected_hour)
tab1, tab2, tab3 = st.tabs(['Number of docks in Barcelona', 'Density Maps', 'Number of bikes through time'])

with tab1:
    st.title("Bicing Barcelona")
    years = df['year'].unique()
    year = st.slider('Year', min_value=2019, max_value=2022, step=1)

    df_new = df[df['year'] == year]
    st.map(df_new)

with tab2:
    st.title("Density Map")
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=df_density['lat'].mean(),
            longitude=df_density['lon'].mean(),
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=df_density,
                get_position='[lon, lat]',
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=df_density,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
    ))

with tab3:
    st.title('Other Views')

    bike_counts = df.value_counts(subset=['month', 'year', Y_COLUMN]).rename('count').reset_index()
    c = ['red', 'blue', 'green', 'orange', 'purple']
    fig, ax = plt.subplots(figsize=(10, 6))
    g = sns.lineplot(data=bike_counts, x='month', y=Y_COLUMN, hue='year', palette=c, ax=ax)
    ax.set_xlabel('Months')
    ax.set_ylabel('Number of bikes available (%)')
    ax.set_title('Number of bikes available by month (%)')
    st.pyplot(fig)

    day_order = list(calendar.day_name)
    df['day_of_week'] = pd.Categorical(df['day_of_week'], categories=day_order, ordered=True)
    bike_counts = df.value_counts(subset=['month', 'day_of_week', Y_COLUMN]).rename('count').reset_index()
    c = ['red', 'blue', 'green', 'orange', 'purple']
    fig, ax = plt.subplots(figsize=(10, 6))
    g = sns.lineplot(data=bike_counts, x='day_of_week', y=Y_COLUMN, hue='month', palette="rocket", ax=ax)
    ax.set_xlabel('day_of_week')
    ax.set_ylabel('Number of bikes available (%)')
    ax.set_title('Number of bikes available by week (%)')
    ax.legend()
    st.pyplot(fig)

    bike_counts = df.value_counts(subset=['hour', 'day_of_week', Y_COLUMN]).rename('count').reset_index()
    c = ['red', 'blue', 'green', 'orange', 'purple']
    fig, ax = plt.subplots(figsize=(10, 6))
    g = sns.lineplot(data=bike_counts, x='hour', y=Y_COLUMN, hue='day_of_week', palette="rocket", ax=ax)
    ax.set_xlabel('Hours')
    ax.set_ylabel('Number of bikes available (%)')
    ax.set_title('Number of bikes available by hour (%)')
    ax.legend()
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.set(style='ticks')
    sns.lineplot(data=df, x='datetime', y=Y_COLUMN, hue='festivo', alpha=0.5, palette="rocket", ax=ax)
    ax.set_xticks(df['hour'].unique())
    ax.set_xticklabels(df['hour'].unique(), rotation=45, ha='right')
    ax.set_title('Number of Available Bikes, sorted by festivo (%)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Bikes')
    ax.legend()
    st.pyplot(fig)
