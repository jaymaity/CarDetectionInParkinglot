'''Code for fine-tuning Inception V3 for a new task.

Start with Inception V3 network, not including last fully connected layers.

Train a simple fully connected layer on top of these.


'''
import os
import numpy as np
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Dropout
import inception_v3 as inception

N_CLASSES = 3
IMSIZE = (299, 299)

# TO DO:: Replace these with paths to the downloaded data.
# Training directory
train_dir = '/home/jay/Downloads/sport3/train'
# Testing directory
test_dir = '/home/jay/Downloads/sport3/validation'


# Start with an Inception V3 model, not including the final softmax layer.
base_model = inception.InceptionV3(weights='imagenet')
print 'Loaded Inception model'

# Turn off training on base model layers
for layer in base_model.layers:
    layer.trainable = False

# Add on new fully connected layers for the output classes.
x = Dense(32, activation='relu')(base_model.get_layer('flatten').output)
x = Dropout(0.5)(x)
predictions = Dense(N_CLASSES, activation='softmax', name='predictions')(x)

model = Model(input=base_model.input, output=predictions)

model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])


# Show some debug output
print (model.summary())

print 'Trainable weights'
print model.trainable_weights


# Data generators for feeding training/testing images to the model.
train_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(
        train_dir,  # this is the target directory
        target_size=IMSIZE,  # all images will be resized to 299x299 Inception V3 input
        batch_size=32,
        class_mode='categorical')

test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(
        test_dir,  # this is the target directory
        target_size=IMSIZE,  # all images will be resized to 299x299 Inception V3 input
        batch_size=32,
        class_mode='categorical')

model.fit_generator(
        train_generator,
        samples_per_epoch=32,
        nb_epoch=5,
        validation_data=test_generator,
        verbose=2,
        nb_val_samples=80)
model.save_weights('sport3_pretrain.h5')  # always save your weights after training or during training


rootdir = "/home/jay/Downloads/sport3/validation/"

# for subdir, dirs, files in os.walk(rootdir):
#     for file in files:
#         img_path = os.path.join(subdir, file)
#         #img_path = '/home/jay/Downloads/sport3/validation/hockey/img_2997.jpg'
# 	img = image.load_img(img_path, target_size=IMSIZE)
# 	x = image.img_to_array(img)
# 	x = np.expand_dims(x, axis=0)
#
# 	x = inception.preprocess_input(x)
#
# 	preds = model.predict(x)
# 	print('Predicted:', preds)


def generate_html_file(rootdir, no_of_image_per_page, output_path):

    os.makedirs(os.path.dirname(output_path))

    initial_html = "<html><body><style type=\"text/css\"> \
        img.resize{width: 250px; height: 250px;}\.tdSize{width: 50px; vertical-align: top;} \
        table, th, td {border: 1px solid black;}</style>" \
        "<table>"\
        "<tr><th class=\"tdSize\">Image</th><th class=\"tdSize\" colspan=3>Prediction</th> </tr>"

    if no_of_image_per_page is None:
        save_all_images(rootdir, initial_html, output_path)
    else:
        save_image_per_page(rootdir, initial_html, output_path, no_of_image_per_page)

def save_image_per_page(rootdir, initial_html, output_path, img_per_page):
    count  = 0
    part = 1
    html = initial_html
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            img_path = os.path.join(subdir, file)
            img = image.load_img(img_path, target_size=IMSIZE)
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)

            x = inception.preprocess_input(x)

            preds = model.predict(x)
            #preds = [0.783478233, 0.237423644, 0.090009]
            html += get_html_from_image(preds[0], img_path)
            count += 1
            if(count == img_per_page):
                save_file(html, part, output_path)
                part += 1
                count = 0


def save_all_images(initial_html, output_path):
    html = initial_html
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            img_path = os.path.join(subdir, file)
            img = image.load_img(img_path, target_size=IMSIZE)
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)

            x = inception.preprocess_input(x)

            preds = model.predict(x)
            #preds = [0.783478233, 0.237423644, 0.090009]
            html += get_html_from_image(preds[0], img_path)
    html += "</table></body></html>"

    text_file = open(output_path + "/ImagePrediction_Home.html", "w")
    text_file.write(html)
    text_file.close()

def save_file(html, part, output_path):
    html += "</table></body></html>"
    text_file = open(output_path + "/ImagePrediction_Home_" + str(part) + ".html", "w")
    text_file.write(html)
    text_file.close()



def get_html_from_image(prediction_array, image):
    str_html  = "<tr><td>" \
                + "<img class =\"resize\" src='"+image+"' />"\
                +"</td>"\
                +"<td class=\"tdSize\">"+str(prediction_array[0])\
                +"</td><td class=\"tdSize\">"+str(prediction_array[1])\
                +"</td><td class=\"tdSize\">"+str(prediction_array[2])+"</td></tr>"
    return str_html

# Set this count to None to output all images in one file
count = 100
#count = None

generate_html_file(rootdir, count, os.curdir+"/htmloutput/")

