import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import seaborn as sns
#df 
st.set_page_config(layout='wide')
import pandas as pd
import glob
import calendar
import matplotlib.pyplot as plt

@st.cache_data
def init_connection():
    path = 'C:/Users/nanay/Documents/Màster/capstone/'
    df = pd.read_csv('merged_df.csv')
    df['date'] = pd.to_datetime(df['last_updated_hour']).dt.date
    df['Holiday'] = df['DataInici'].notnull().astype(bool)
    df['total bikes'] = df['num_bikes_available'] + df['num_docks_available']  # se debe comparar el total bikes con capacity pero no puedo compararlos porque tus datos ya estan agrupados por hora

    df['percentatge'] = (df['num_bikes_available'] /  df['total bikes'])
    df = df[df['percentatge'] <= 1]
    df['last_updated_hour'] = pd.to_datetime(df['last_updated_hour'])
    df['day of the week'] = df['last_updated_hour'].dt.day_name()
    df = df[['num_bikes_available','lat','lon','date','month','day of the week','percentatge','hour','year','Holiday']]
    df_2 = df.sample(n=400000)
    return df_2

df = init_connection()



col1, col2, col3 = st.columns(3)
df.replace({pd.NA: None}, inplace=True)
unique_days = df['day of the week'].unique()
df['month_name'] = pd.to_datetime(df['month'], format='%m').dt.strftime('%B')
months =df['month_name'].unique()
day = col1.selectbox('Day of the week', options=unique_days)
month = col2.selectbox('Month', options=months)
values = col3.slider('Select an hour slice',min_value=0, max_value=24, step=1)
df_density = df[df['day of the week'] == day]
df_density= df_density[df_density['month_name'] == month]
df_density= df_density[df_density['hour'] == values]
tab1,tab2, tab3 = st.tabs(['Number of docks in Barcelona','Density Maps','Number of bikes through time'])


with tab1:
    st.title("Bycing Barcelona")
    years = df['year'].unique()
    year = st.slider('Year', min_value=2019,max_value=2022,step=1)

    df_new = df[df['year'] == year ]
    st.map(df_new)

with tab2:
    st.title("Density Map")


    df_density = df_density.to_json(orient='records')
    df_density = pd.read_json(df_density)
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

    bike_counts = df.value_counts(subset=['month', 'year', 'percentatge']).rename('count').reset_index()
    c = ['red', 'blue', 'green', 'orange', 'purple']
    fig, ax = plt.subplots(figsize=(10, 6))
    g = sns.lineplot(data=bike_counts, x='month', y='percentatge', hue='year', palette=c, ax=ax)
    ax.set_xlabel('Months')
    ax.set_ylabel('Number of bikes available (%)')
    ax.set_title('Number of bikes available by month (%)')
    st.pyplot(fig)


    day_order = list(calendar.day_name)
    df['day of the week'] = pd.Categorical(df['day of the week'], categories=day_order, ordered=True)
    bike_counts = df.value_counts(subset=['month', 'day of the week', 'percentatge']).rename('count').reset_index()
    c = ['red', 'blue', 'green', 'orange', 'purple']
    fig, ax = plt.subplots(figsize=(10, 6))
    g = sns.lineplot(data=bike_counts, x='day of the week', y='percentatge', hue='month', palette="rocket", ax=ax)
    ax.set_xlabel('Day of the week')
    ax.set_ylabel('Number of bikes available (%)')
    ax.set_title('Number of bikes available by week (%)')
    ax.legend()
    st.pyplot(fig)


    bike_counts = df.value_counts(subset=['hour', 'day of the week', 'percentatge']).rename('count').reset_index()
    c = ['red', 'blue', 'green', 'orange', 'purple']
    fig, ax = plt.subplots(figsize=(10, 6))
    g = sns.lineplot(data=bike_counts, x='hour', y='percentatge', hue='day of the week', palette="rocket", ax=ax)
    ax.set_xlabel('Hours')
    ax.set_ylabel('Number of bikes available (%)')
    ax.set_title('Number of bikes available by hour (%)')
    ax.legend()
    st.pyplot(fig)


    fig, ax = plt.subplots(figsize=(10, 6))
    sns.set(style='ticks')
    sns.lineplot(data=df, x='date', y='percentatge', hue='Holiday', alpha=0.5, palette="rocket", ax=ax)
    ax.set_xticks(df['hour'].unique())
    ax.set_xticklabels(df['hour'].unique(), rotation=45, ha='right')
    ax.set_title('Number of Available Bikes, sorted by Holiday (%)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Bikes')
    ax.legend()
    st.pyplot(fig)