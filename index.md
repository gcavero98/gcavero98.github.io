# Capstone project: Bicing
## Preprocessing
### Stations dataset
Después de un análisis de los datos descargados, decidimos **eliminar** aquellos registros que cumpliesen una o más de las siguientes condiciones:
- NaN values
- df[df['num_bikes_available'] != df['num_bikes_available_types.mechanical'] + df['num_bikes_available_types.ebike']]
- df[df['status'] != 'IN_SERVICE']
- df[df['is_installed' != 1]]
- df[df['is_renting' != 1]]
- df[df['is_returning' != 1]]

df['last_updated'] i df['ttl'] -> YYYY-MM-DD HH:MM:SS format.

Dado que los datos de validación están en formato **horario**, hemos resampleado los datos a la misma frecuencia temporal, promediando los valores de ocupación durante esa hora.

### Information dataset
Usamos las columnas ['lat', 'lon', 'altitude', 'post_code'] (merge con el dataset **Stations**).
### Data Analysis
[stations_per_months]()
[stations_per_day_of_week]()
[correlation_with_shifted_timestamps](images/)

### Climate dataset
Hemos añadido datos climáticos (**ERA5 reanalysis**, ECMWF):
- 1h resolución temporal, 0.25º resolución espacial.
- **Temperatura a 2m**, precipitación, intensidad del viento a 10m, cloud cover.
[temperature](images/...)

## Predictions
Motivados por los gráficos anteriores, donde se puede apreciar un comportamiento distinto entre estaciones, decidimos hacer un modelo por estación. Además, se utilizó un regresor global para poder predecir las estaciones que no estuvieran en el dataset de training.
### Transformations
- 'month' (4BinsDIscretizer, encode='onehot')
- 'hour' (12BinsDIscretizer, encode='ordinal')

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
- split: TimeSeriesSplit(n_split=5) para no entrenar con datos del futuro
- regressor: hemos probado KNN, random forest, pero obtuvimos mejores resultados con una **Linear Regression**

Viendo los coeficientes asociados a cada feature, descartamos aquellos con un coeficiente cercano a 0, quedándonos con las siguientes features:
- sdf
- sdf
- asdf
- asdf
- asdf


Resultados validación: [-0.125, -0.116, -0.098, -0.119, -0.099]





