from __future__ import division, print_function
import sys
import glob
import re
import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
import os, os.path
import csv
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras import applications
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from colorthief import ColorThief
from sklearn.cluster import KMeans
from google_images_download import google_images_download
from flask import jsonify
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.wsgi import WSGIServer
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image


app = Flask(__name__)


print('Server started')

def get_dominant_colors(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((image.shape[0]*image.shape[1],3))

    clt = KMeans(n_clusters=6)
    clt.fit(image)

    (histogram, _) = np.histogram(clt.labels_, bins=np.arange(0,len(np.unique(clt.labels_))+1))
    histogram = histogram.astype("float")
    histogram /= histogram.sum()

    dmp = np.zeros((300, 300, 3), dtype="uint8")
    i = 0

    for (p, c) in zip(histogram, clt.cluster_centers_):
        j = i+(p*300)
        cv2.rectangle(dmp, (int(i), 0), (int(j), 300), c.astype("uint8").tolist(), -1)
        i = j

    plt.figure()
    plt.axis("off")
    plt.imshow(dmp)

    import time
    randint = str(int(time.time()))

    plt.savefig('./static/downloads/{}topk.jpg'.format(randint))
    return randint



def download_images_by_url(output_dir, url, limit):
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    response = google_images_download.googleimagesdownload()
    response.download({
        "similar_images": url,
        "color_type": "transparent",
        "size": "medium",
        "limit": limit,
        "output_directory": output_dir,
        "chromedriver": "/usr/local/bin/chromedriver"})



def download_display_images(id):
    print('id is: {}'.format(id))
    with open('./part1.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        counter = 0
        for row in csvReader:
            if id == row[0]:
                print('The url is: {}'.format(row[1]))
                download_images_by_url('static/', row[1], 4)

def predict_helper(image_path):

    path = get_dominant_colors(image_path)

    model = applications.VGG16(weights='imagenet', include_top=False)
    classes = np.load('classes.npy').item()
    classes_map = {value: key for key, value in classes.items()}
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = image/255
    image = np.expand_dims(image, axis=0)
    vgg16_result = model.predict(image)

    model = Sequential()
    model.add(Flatten(input_shape=vgg16_result.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(classes), activation='sigmoid'))
    model.load_weights('./models/model.h5')

    class_predicted = model.predict_classes(vgg16_result)
    label = classes_map[class_predicted[0]]
    return {
        'preds': label,
        'path': path
    }


def predict(image_path):
    full_path = '/Users/kevinshi/Downloads/webapp/' + image_path
    print(full_path)
    result = predict_helper(full_path)
    preds = result['preds']

    download_display_images(preds)
    links = ""
    with open('./part1.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        counter = 0
        for row in csvReader:
            if row[0] == preds:
                links = row[1]
                break

    print('The predicted output is: ')
    print(preds)
    return {
        'preds': preds,
        'links': links,
        'path': result['path']
    }


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        import shutil
        if os.path.exists('./static/downloads'):
            shutil.rmtree('./static/downloads')
        os.mkdir('./static/downloads')

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        result = predict(file_path)
        files = os.listdir("./static/downloads")
        files = ["./static/downloads/" + x for x in files]

    return jsonify({
        'preds': result['preds'],
        'links': result['links'],
        'imgs': files,
        'path': ["./static/downloads/" + result['path'] + ".jpg"]
    })


if __name__ == '__main__':
    http_server = WSGIServer(('', 18888), app)
    http_server.serve_forever()
