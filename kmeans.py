import numpy as np
import pandas as pd
from osgeo import gdal, gdal_array, osr
from sklearn import cluster

# Tell GDAL to throw Python exceptions, and register all drivers
gdal.UseExceptions()
gdal.AllRegister()

band =  range(1,4)
# Read in raster image 
img_ds = gdal.Open('D:/Data Science/agro_meta/img/imagengrande.tiff')
# height 223, width 458

# coordenadas de la foto
# ver como usar esto 
# RAROOOOO esos vlaores. me manda a neuquen
xoffset, px_w, rot1, yoffset, rot2, px_h = img_ds.GetGeoTransform()

x = 200
y = 140

posX = px_w * x + rot1 * y + xoffset
posY = rot2 * x + px_h * y + yoffset

# meta data
from PIL import Image
from PIL.TiffTags import TAGS

with Image.open('D:/Data Science/agro_meta/img/imagengrande.tiff') as img:
    meta_dict = {TAGS[key] : img.tag[key] for key in img.tag.keys()}

# nos quedamos con las 3 bandas rgb
# pasamos a matriz
# convertimos en array
bands = []
img = []
X = []
for i,j in enumerate(band):
    bands.append(img_ds.GetRasterBand(j))
    img.append(bands[i].ReadAsArray())
    X.append(img[i].reshape((-1,1)).ravel())

# cerramos la foto
img_ds = None

# dataframe cuya columnas son rgb
names =  ['R','G','B']
df = pd.DataFrame.from_dict(dict(zip(names, X)))

df.head()

k_means = cluster.KMeans(n_clusters=4)
k_means.fit(df)

X_cluster = k_means.labels_
X_cluster = X_cluster.reshape(img[0].shape)

print (len(X_cluster))


dot = np.ndarray([posX,posY] ,size  = (1,1))

%matplotlib inline  

import matplotlib.pyplot as plt

plt.figure(figsize=(20,20))
plt.imshow(X_cluster, cmap="hsv")

plt.show()