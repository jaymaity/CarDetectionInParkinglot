import sys
import os
import time
import datetime
import json
import shutil

# Adding common folder
sys.path.insert(0, '../common/')
import PredictParkingLot as pdt


class ContiniousPrediction:

    config = None
    input_image_path = None
    output_data_path = None
    output_file = None
    interval = None
    move_image_path = None
    move_predicted_images = None
    is_live = None

    def __init__(self):
        """
        Get config data from filess
        """

        # Reading values from config file
        with open('../common/configs/live.config') as config_file:
            self.config = json.load(config_file)

        self.input_image_path = self.config["InputImagePath"]
        self.output_data_path = self.config["OutputDataPath"]
        self.output_file = self.config["OutputFileName"]
        self.interval = self.config["Interval"]
        self.move_image_path = self.config["MoveImagePath"]
        self.move_predicted_images = self.config["MovePredictedImages"]
        self.is_live = self.config["IsLive"]
        self.is_move_img = self.config["MovePredictedImages"]


    def on_folder(self):
        """
        Predict all images in a folder path
        Press Cntl + c to exit from the code
        :return:
        """
        pred = pdt.PredictParkingLot()
        filejson = dict()

        while True:
            files = []
            for (dirpath, dirnames, filenames) in os.walk(self.input_image_path):
                files.extend(filenames)

            for file_ins in files:
                predval = None
                timebefore = datetime.datetime.now()

                try:
                    predval = pred.predict_full_image(self.input_image_path+file_ins)
                    if self.is_move_img:
                        shutil.move(self.input_image_path + file_ins, self.move_image_path + file_ins)
                except:
                    print(file_ins+ ": Image Broken, Trying new Image")

                timeafter = datetime.datetime.now()

                predtime = timeafter - timebefore

                filejson["islive"] = self.config["IsLive"]
                filejson["filename"] = file_ins
                filejson["preddata"] = predval
                filejson["predtime"] = predtime.microseconds

                text_file = open(self.output_data_path + self.output_file, "w")
                text_file.write(str(filejson).replace("'","\"").replace("u\"","\""))
                text_file.close()

                if self.interval > 0:
                    print("Taking "+str(self.interval)+" seconds time off")
                    time.sleep(self.interval)
