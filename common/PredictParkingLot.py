""" Predict Parking lot images for free/occupied spots"""

import os
import json
import numpy as np
from keras.preprocessing import image
from keras.models import load_model
import inception_v3 as inception
import imageprocess.imagesplit as imagesplit


class PredictParkingLot:
    """
    Predict Parking lot image
    """

    model = None
    config = None
    model_path = None
    image_size = None
    intermediate_image_path = None
    map_path = None

    def __init__(self):
        """
        Initialize variables
        """

        self.image_size = (299, 299)

        # Reading values from config file
        with open('../common/configs/pred.config') as config_file:
            self.config = json.load(config_file)

        self.model_path = self.config["WeightPath"]
        self.intermediate_image_path = self.config["IntermediateImages"]
        self.map_path = self.config["MapPath"]

        if self.model is None:
            self.model = self.get_model()

    def get_model(self):
        """
        Load model and returns the model
        :return:
        """
        model1 = load_model(self.model_path)
        model1.compile(loss='binary_crossentropy',
                       optimizer='sgd',
                       metrics=['accuracy'])
        return model1

    def predict_single(self, img_path, is_print_pred=True):
        """
        Predicts single image to it's chances
        :param img_path: Path of the image to classify
        :param model: Pre-compiled model
        :return:
        """
        img = image.load_img(img_path, target_size=self.image_size)
        resized_img = image.img_to_array(img)
        resized_img = np.expand_dims(resized_img, axis=0)
        resized_img = inception.preprocess_input(resized_img)
        predicted_data = self.model.predict(resized_img)

        # Formatting the result
        occupied = np.array(predicted_data[:, 0])
        vacant = np.array(predicted_data[:, 1])

        predicted_data = {'Occupied': occupied[0], 'Vacant': vacant[0]}

        # Print prediction after each prediction
        if is_print_pred:
            print(predicted_data)
        return predicted_data

    def predict_full_image(self, img_path):
        """
        Split the image and predict each component
        :param img_path: Path of the original image
        :return:
        """
        img_splt = imagesplit.imagesplit()
        output_path = img_splt.split_image(img_path,
                                           self.map_path,
                                           self.intermediate_image_path)
        files = []

        lot = dict()

        for (dirpath, dirnames, filenames) in os.walk(output_path):
            files.extend(filenames)

        for file_ins in files:
            pred = self.predict_single(output_path+file_ins)
            lot[os.path.splitext(file_ins)[0]] = pred
        return lot

# img_splt = imagesplit.imagesplit()
# output_path = img_splt.split_image("/home/jay/BigData/ML/parkinglot/web/static/images/input/11-25 17.12.17.jpg",
#                                    "/home/jay/BigData/ML/parkinglot/common/configs/imagemap/",
#                                    "/home/jay/BigData/ML/parkinglot/web/static/images/intermediate/")