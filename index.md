# Capstone project: Bicing
## Preprocessing
### Stations dataset
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

### Information dataset
Usamos las columnas ['lat', 'lon', 'altitude', 'post_code'] (merge con el dataset **Stations**).

### Climate dataset 
Hemos añadido datos climáticos (ERA5 reanalysis data, ECMWF):
- 1h resolución temporal, 0.25º resolución espacial.
- Temperatura a 2m, precipitación, intensidad del viento a 10m.

*presentación: plot de la variable que más nos correlacione (si finalmente nos ayuda en la predicción)*

## Predictions
### Transformations
- 'month' (4BinsDIscretizer, encode='onehot')
- 'hour' (4BinsDIscretizer, encode='onehot')

Además de las disponibles, añadimos las siguientes features:
- 'percentage_docks_available'
- 'percentage_docks_available' shifted 1, 2, 3 and 4 hours (StandardScaler)
- 'is_summer' (OneHotEncoder)
- 'is_weekend' (OneHotEncoder)
- 'is_night' (OneHotEncoder)
- 'day_of_week'
- 'is_work_morning'

### Cross Validation
- scoring: 'neg_root_mean_squared_error'
- split: TimeSeriesSplit(n_split=5)
- regressor: linear_model.LinearRegression
  
Resultados validación: [-0.12541932, -0.11604383, -0.09883015, -0.11936493, -0.09962058]


