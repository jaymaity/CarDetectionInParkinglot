import Predict as pdt
import os
import time
import datetime

INPUT_IMAGE_PATH = "/home/jay/BigData/MLProj732/dl/static/source"
OUTPUT_DATA_PATH = "/home/jay/BigData/MLProj732/dl/static/data/"
INTERVAL = 1

pred = pdt.Predict()

files = []

filejson = dict()

for (dirpath, dirnames, filenames) in os.walk(INPUT_IMAGE_PATH):
    files.extend(filenames)

while True:

    for file in files:
        timebefore = datetime.datetime.now()
        predval = pred.predict_full_image(os.path.splitext(file)[0])
        timeafter = datetime.datetime.now()

        predtime = timeafter - timebefore

        filejson["filename"] = file
        filejson["preddata"] = predval
        filejson["predtime"] = predtime.microseconds

        text_file = open(OUTPUT_DATA_PATH + "Output.txt", "w")
        text_file.write(str(filejson).replace("'", "\""))
        text_file.close()

        print("Taking "+str(INTERVAL)+" seconds time off")
        time.sleep(INTERVAL)

