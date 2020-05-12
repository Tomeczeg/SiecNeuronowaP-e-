# -*- coding: utf-8 -*-
"""Lab02.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LoRNda1oF7N5vooMy25DSIqY-KsgMT6J
"""

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
drive.mount('/gdrive')
# %cd /gdrive
# %cd '/gdrive/My Drive/Colab Notebooks/baza'

!pip show tensorflow

!pip show keras
import csv
#from tensorflow import keras
import glob, os

# For the current version: 
#!pip install --upgrade tensorflow

# For a specific version:
!pip install tensorflow==1.14

!pip install keras==2.2.4

#Bibioteki do obliczen tensorowych
import tensorflow as tf
from tensorflow import keras

#import plaidml.keras
#plaidml.keras.install_backend()

#Bibioteka do obsługi sieci neuronowych
import keras

#Załadowania bazy uczącej
import imageio
import numpy as np

import os

from keras.models import load_model

Count= 70
Size= 7
Data_size=2
BazaVec = np.empty((Count,Size,1))
BazaAns = np.empty((Count,1))
table={}
i=0
start_pl_index=12540
end_pl_index=12609
with open('data.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        table[i]=row
        i=i+1
z1=0
for l in range(start_pl_index,end_pl_index-6):
    for j in range(7):
        BazaVec[z1,j,:]=float(table[l+j][4]) # dzienny przyrost 
    BazaAns[z1]=float(table[l+7][4])
    z1=z1+1
max_answer=np.amax(BazaAns)/2
print(max_answer)
exit()

BazaAns=BazaAns/max_answer-1
BazaAns=BazaAns[0:z1]
maxval = np.amax(BazaVec)/2
BazaVec=BazaVec/max_answer-1
BazaVec=BazaVec[0:z1,:,:]
#
##Stworzenia modelu sieci
inputt = keras.engine.input_layer.Input(shape=(Size,1),name="wejscie")
#
FlattenLayer = keras.layers.Flatten()
#
path = FlattenLayer(inputt)

for i in range(0,5):
  LayerDense1 = keras.layers.Dense(12, activation=None, use_bias=True, kernel_initializer='glorot_uniform')
  path = LayerDense1(path)
  LayerPReLU1 = keras.layers.PReLU(alpha_initializer='zeros', shared_axes=None)
  path = LayerPReLU1(path)
#
LayerDenseN = keras.layers.Dense(1,activation=None, use_bias=True, kernel_initializer='glorot_uniform')
output = LayerDenseN(path)
##---------------------------------
## Creation of TensorFlow Model
##---------------------------------
covidModel = keras.Model(inputt, output, name='covidEstimatior')
#
covidModel.summary() # Display summary
#
##Włączenia procesu uczenia
#
rmsOptimizer = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)

#
covidModel.compile(optimizer=rmsOptimizer,loss=keras.losses.mean_absolute_error)
#covidModel.compile(optimizer=rmsOptimizer,loss=keras.losses.binary_crossentropy,metrics=['accuracy'])
#

covidModel.fit(BazaVec, BazaAns, epochs=150, batch_size=10, shuffle=True)
covidModel.save('covid.h5')
##Przetestować / użyć sieci

BazaVecW = BazaVec[z1-1:z1,:,:]
covid = covidModel.predict(BazaVecW)
print((covid[0]+1)*max_answer)
tekst=open('Przewidywania.txt', 'w')
tekst.write("Przewidywana liczba przypadków na dzień 11.05.2020 r. w Polsce to"+ str( (covid[0]+1)*max_answer))
tekst.close()

