import Predict as pdt
import os
import time
import datetime
import shutil

import numpy as np
INPUT_IMAGE_PATH = "/home/jay/BigData/MLProj732/dl/static/source"
OUTPUT_DATA_PATH = "/home/jay/BigData/MLProj732/dl/static/data/"
LIVE_DATA_PATH = "/home/jay/BigData/MLProj732/dl/static/datalive/"
LIVE_DATA_BACKUP = "/home/jay/BigData/MLProj732/dl/static/datalivebackup/"
INTERVAL = 1

pred = pdt.Predict()

files = []

filejson = dict()

while True:
    files = []
    for (dirpath, dirnames, filenames) in os.walk(LIVE_DATA_PATH):
        files.extend(filenames)
    for file in files:
        predval = None
        timebefore = datetime.datetime.now()
        try:
            predval = pred.predict_full_image(os.path.splitext(file)[0], is_live=True)
            shutil.move(LIVE_DATA_PATH + file, LIVE_DATA_BACKUP + file)
        except:
            print("Image Broken Trying new Image")
        timeafter = datetime.datetime.now()

        predtime = timeafter - timebefore



        filejson["islive"] = 1
        filejson["filename"] = file
        filejson["preddata"] = predval
        filejson["predtime"] = predtime.microseconds

        text_file = open(OUTPUT_DATA_PATH + "Output.txt", "w")
        text_file.write(str(filejson).replace("'", "\""))
        text_file.close()



