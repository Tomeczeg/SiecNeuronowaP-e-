from google.colab import drive
drive.mount('/gdrive')
%cd /gdrive
%cd '/gdrive/My Drive/Colab Notebooks/baza'

!pip show tensorflow

!pip show keras

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

# returns a compiled model
# identical to the previous one
genderModel = load_model('siec.h5')
genderModel.summary() # Display summary

ImgCount = 50
ImgWidth = 100
ImgHeight = 100
realwoman=0
realman=0
womanasman=0
manaswoman=0

BazaImg = np.empty((50,ImgHeight,ImgWidth,3))
dirList = os.listdir("baza_testowa//K")
i=0
for dir in dirList:
  print("k", dir)
  FileName = "baza_testowa//K//{}".format(dir)
  Img = imageio.imread(FileName)
  Img = (Img / 127.5) - 1
  BazaImg[i,:,:,:] = Img[0:ImgHeight,0:ImgWidth,0:3]
  i=i+1
  if i>=ImgCount/2:
    break

dirList = os.listdir("baza_testowa//M")
for dir in dirList:
  print("m", dir)
  FileName = "baza_testowa//M//{}".format(dir)
  Img = imageio.imread(FileName)
  Img = (Img / 127.5) - 1
  BazaImg[i,:,:,:] = Img[0:ImgHeight,0:ImgWidth,0:3]
  i=i+1
  if i>=ImgCount:
    break

gender = genderModel.predict(BazaImg) # 0 - m, 1 - k
print(gender)
for j in range(ImgCount):
  if(j<ImgCount/2):
    if(gender[j]>=0.5):
      realwoman=realwoman+1
    else:
      womanasman=womanasman+1
  else:
    if(gender[j]<0.5):
      realman=realman+1
    else:
      manaswoman=manaswoman+1

print("liczba kobiet zaklasyfikowanych jako kobiety", realwoman)
print("liczba kobiet zaklasyfikowanych jako mezczyzni", womanasman)
print("liczba mezczyzn zaklasyfikowanych jako mezczyzni", realman)
print("liczba mezczyzn zaklasyfikowanych jako kobiety", manaswoman)
tekst=open('wynik_sieci.txt', 'w')
tekst.write("+-----------------------+----------------------+\n")
tekst.write("|                       | Faktyczna płeć osoby |\n")
tekst.write("|                       | na zdjęciu           |\n")
tekst.write("+                       +----------+-----------+\n")
tekst.write("|                       |  Kobieta | Mężczyzna |\n")
tekst.write("+-----------+-----------+----------+-----------+\n")
tekst.write("| Odpowiedź |  Kobieta  |    "+ str(realwoman)+"    |     "+str(manaswoman)+"    |\n")
tekst.write("| sieci     +-----------+----------+-----------+\n")
tekst.write("|           | Mężczyzna |     "+str(womanasman)+"    |     "+str(realman)+"    |\n")
tekst.write("+-----------+-----------+----------+-----------+\n")
tekst.close()
#50
#--------------------------------
# Prawdziwa Płeć | Odpowiedz sieci
#----------------+---------+------
#                |   M     |  K
#----------------+---------+------
#   M            |         |  1
#----------------+---------+------
#   K            |         |  1

#ImgCount = 100
#ImgWidth = 100
#ImgHeight = 100
#
#BazaImg = np.empty((ImgCount,ImgHeight,ImgWidth,3))
#BazaAns = np.empty((ImgCount)) # 0 - m, 1 - k
#dirList = os.listdir(".\\baza\\m")
#i=0
#for dir in dirList:
#  print(dir)
#  FileName = ".\\baza\\m\\{}".format(dir)
#  Img = imageio.imread(FileName)
#  Img = (Img / 127.5) - 1
#  BazaImg[i,:,:,:] = Img[0:ImgHeight,0:ImgWidth,0:3]
#  BazaAns[i] = 0
#  i=i+1
#  if i>=ImgCount/2:
#    break
#
#dirList = os.listdir(".\\baza\\k")
#for dir in dirList:
#  print(dir)
#  FileName = ".\\baza\\k\\{}".format(dir)
#  Img = imageio.imread(FileName)
#  Img = (Img / 127.5) - 1
#  BazaImg[i,:,:,:] = Img[0:ImgHeight,0:ImgWidth,0:3]
#  BazaAns[i] = 1
#  i=i+1
#  if i>=ImgCount:
#    break
#
#BazaImg = BazaImg[0:i,:,:,:]
#BazaAns = BazaAns[0:i]
#print(BazaImg.shape)
#
##Stworzenia modelu sieci
#
#input  = keras.engine.input_layer.Input(shape=(ImgHeight,ImgWidth,3),name="wejscie")
#
#FlattenLayer = keras.layers.Flatten()
#
#path = FlattenLayer(input)
#
#for i in range(0,6):
#  LayerDense1 = keras.layers.Dense(50, activation=None, use_bias=True, kernel_initializer='glorot_uniform')
#  path = LayerDense1(path)
#
#  LayerPReLU1 = keras.layers.PReLU(alpha_initializer='zeros', shared_axes=None)
#  path = LayerPReLU1(path)
#
#LayerDenseN = keras.layers.Dense(1, activation=keras.activations.sigmoid, use_bias=True, kernel_initializer='glorot_uniform')
#output = LayerDenseN(path)
#
##---------------------------------
## Creation of TensorFlow Model
##---------------------------------
#genderModel = keras.Model(input, output, name='genderEstimatior')
#
#genderModel.summary() # Display summary
#
##Włączenia procesu uczenia
#
#rmsOptimizer = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
#
#genderModel.compile(optimizer=rmsOptimizer,loss=keras.losses.binary_crossentropy,metrics=['accuracy'])
#
#genderModel.fit(BazaImg, BazaAns, epochs=15, batch_size=10, shuffle=True)
#
#genderModel.save('siec.h5')
##Przetestować / użyć sieci
#
