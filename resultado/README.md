
## Datos

Descargamos datos de Sentinel2 para los lotes de entrenamiento y test. Usamos el período octubre-julio de cada campaña y los datos de las bandas B1, B2, B3, B4, B5, B6, B7, B8, B9, B11 y B12.    

Para cada lote generamos un buffer de píxeles alrededor del punto provisto, y resumimos los valores de las bandas con el promedio para cada momento del tiempo. Descartamos lotes clasificados como soja y maíz que tuvieran una baja proporción de vegetación según la metadata de Sentinel. También descartamos lotes con una proporción alta de nubosidad. 

Con la información disponible para cada lote generamos dos imágenes:

1. _Serie de tiempo_. Una imagen que representa el nivel de las bandas a lo largo del tiempo. Cada banda tiene un color distinto y el fondo es negro. Usamos la misma escala del eje vertical para todas las imágenes.

2. _Mapa de calor_. El eje horizontal representa el momento del tiempo y el eje vertical tiene una linea para cada banda desde B1 hasta B12. La intensidad del color de cada celda representa el nivel de la banda en un momento del tiempo. Usamos la misma escala de colores para todas las bandas y para todas las imágenes.

## Modelo

Usamos la arquitectura resnet implementada por la librería [fastai](https://www.fast.ai/) para python. Hicimos múltiples pruebas cambiando hiperparámetros tales como la cantidad de capas, la tasa de aprendizaje, las imágenes usadas como input, la cantidad de epochs, el tamaño de los batch, remuestreo, etc.

El modelo presentado consiste en un ensamble de tres modelos:

1. resnet50 con imágenes de series de tiempo con oversampling de las imágenes para controlar el desbalance
2. resnet50 con imágenes de series de tiempo cambiando la función de pérdida con pesos por clase para controlar el desbalance
3. resnet50 con mapas de calor con oversampling de las imágenes para controlar el desbalance

El ensamble predice la clase mayoritaria de los 3 modelos, y en caso de empate, predice la clase de mayor probabilidad. 

## Pasos

1. Ejecutar import_images_timeseries.ipynb 2 veces:
	* Una vez con `EXPERIMENT_ID = "heatmap_ts"` y `HEATMAP = True` en Parameters
	* Otra vez con `EXPERIMENT_ID = "ts_fullbandas_conX"` y `HEATMAP = False` en Parameters

2. Ejecutar xresnet_timeseries_A.ipynb
	
3. Ejecutar xresnet_timeseries_B.ipynb

3. Ejecutar xresnet_heatmap.ipynb

5. Ejecutar ensemble.ipynb


## Posibles mejoras

* Usar el dato de elevación
* Usar datos de otros satélites
* Identificar y eliminar bandas irrelevantes o redundantes de las imágenes
* Usar otras funciones en lugar del promedio para reducir los pixeles del buffer en cada momento del tiempo
* Construir las imágenes usando las escalas de color (para heatmap) o del eje Y (para time series) en función de los datos de cada lote -- en lugar de usar la misma escala para todas las imágenes como hicimos
* Probar otras arquitecturas
* Mejorar el entrenamiento de la red (sanity checks, regularización, funciones de pérdida, métodos de optimización, etc.)
* Lograr setear la seed para que los entrenamientos sean reproducibles
