# Capstone project: Bicing
## Data Analysis
### Bicing data preprocessing
*aquí supongo que irá información que saquemos de los plots de Nayara*

*presentación: plots Nayara*

Después de un análisis de los datos descargados, decidimos **eliminar** aquellos registros que cumpliesen una o más de las siguientes condiciones:
- NaN values
- df[df['num_bikes_available'] != df['num_bikes_available_types.mechanical'] + df['num_bikes_available_types.ebike']]
- df[df['status'] != 'IN_SERVICE']
- df[df['is_installed' != 1]]
- df[df['is_renting' != 1]]
- df[df['is_returning' != 1]]

df['last_updated'] i df['ttl'] -> YYYY-MM-DD HH:MM:SS format.
Dado que los datos de validación están en formato **horario**, hemos resampleado los datos a la misma frecuencia temporal. 
#### Climate Data 
Hemos añadido datos climáticos (ERA5 reanalysis data, ECMWF):
- 1h resolución temporal, 0.25º resolución espacial.
- Temperatura a 2m, precipitación, intensidad del viento a 10m.

*presentación: plot de la variable que más nos correlacione (si finalmente nos ayuda en la predicción)*

## Predictions
### Transformations
Además de las disponibles, añadimos las siguientes features:
- 'is_summer'
- 'day_of_week'
- 'is_weekend'
- 'is_night'
### Training + Predict
FEATURES = [
    'month',
    'hour',
    'day',
    'day_of_week',
    'is_summer',
    'is_weekend',
    'temperature_2m',
    'total_cloud_cover',
    'total_precipitation',
    'windspeed_10m'
]

Y_COLUMN = 'percentage_docks_available'
  
