#!/usr/bin/env python
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from pathlib import Path
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_addons as tfa
import subprocess
import sys
import matplotlib
import subprocess
matplotlib.use('Agg')
def yeni():
    import matplotlib.pyplot as plt
    loaded_styled_generator = tf.keras.models.load_model('working/saved_model/styled_generator')
    img_height, img_width = 256, 256
    channels = 3
    dosya = open("findpro.txt","r",encoding="utf-8")
    isim=dosya.readline()
    def decode_img(image):
        image = tf.image.decode_jpeg(image, channels=3)
        image = tf.image.resize(image, [img_height, img_width])
        image = (tf.cast(image, tf.float32) / 127.5) - 1
        return image


    def process_path(file_path):

        img = tf.io.read_file(file_path)
        img = decode_img(img)
        return img


    # In[5]:


    list_ds = tf.data.Dataset.list_files('static/images/*.jpg', shuffle=True)
    photo_ds = list_ds.map(process_path, num_parallel_calls=tf.data.experimental.AUTOTUNE).batch(1)

    yeni=photo_ds.take(1)
    img_batch = next(iter(yeni))

    prediction = loaded_styled_generator(img_batch, training=False)[0].numpy()
    prediction = (prediction * 127.5 + 127.5).astype(np.uint8)
    img = img_batch[0]
    img = (img * 127.5 + 127.5).numpy().astype(np.uint8)
    plt.imshow(prediction)
    plt.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False,
                    labelbottom=False, labelleft=False)
    plt.savefig("static/converting/" + isim[0:16].strip() + ".jpg",format="jpg",transparent=True, bbox_inches='tight', pad_inches=0)
    plt.savefig("static/uploaded/" + isim[0:16].strip() + ".jpg",format="jpg",transparent=True, bbox_inches='tight', pad_inches=0)
    plt.close()
    def satir_sil(dosya, satir):
        with open(dosya, "r", encoding="utf-8") as d:
            oku = d.readlines()
        with open(dosya, "w", encoding="utf-8") as d:
            for index, line in enumerate(oku):
                if index == satir:
                    d.write("")
                else:
                    d.write(line)
    satir_sil("findpro.txt", 0)
    stop_python_file()
    return isim
def stop_python_file():
    p = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], capture_output=True, text=True)
    lines = p.stdout.split('\n')
    for line in lines:
        if 'adsc.py' in line:
            pid = int(line.split()[1])
            subprocess.run(['taskkill', '/F', '/PID', str(pid)])
            break