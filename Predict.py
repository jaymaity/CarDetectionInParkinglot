import numpy as np
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Activation, Flatten, Dropout
import inception_v3 as inception
import imageprocess.imagesplit as imagesplit
# import tensorflow as tf
# import glob
# import time
import os

IMSIZE = (299, 299)

MODEL_PATH = "/home/jay/BigData/MLProj732/dl/Total_model1.h5"

class Predict:

    model = None

    def __init__(self):
        if self.model is None:
            self.model = load_model(MODEL_PATH)
            self.model.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])

    def get_model(self):
        model1 = load_model(MODEL_PATH)
        model1.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])
        return model1

    def predict_single(self, img_path):
        """
        Predicts single image to it's chances
        :param img_path: Path of the image to classify
        :param model: Pre-compiled model
        :return:
        """
        img = image.load_img(img_path, target_size=IMSIZE)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = inception.preprocess_input(x)
        preds = self.model.predict(x)

        p1 = np.array(preds[:, 0])
        p2 = np.array(preds[:, 1])

        data = {'Occupied': p1[0], 'Vacant': p2[0]}
        print(data)
        return data

    def predict_full_image(self, img_path, is_live=False):
        """
        Split the image and predict each component
        :param img_path: Path of the original image
        :return:
        """
        #split_img_obj = imagesplit.imagesplit(is_live)
        output_path = imagesplit.imagesplit.split_sfu_image(img_path, is_live)
        files = []

        lot = dict()

        for (dirpath, dirnames, filenames) in os.walk(output_path):
            files.extend(filenames)

        for file in files:
            pred = self.predict_single(output_path+file)
            lot[os.path.splitext(file)[0]] = pred
        return lot
