from PIL import Image
import os


class imagesplit:
    INPUT_IMAGE_PATH = "/home/jay/BigData/MLProj732/dl/static/source/"
    INPUT_MAP_PATH = "/home/jay/BigData/MLProj732/dl/imageprocess/imagemap"
    OUTPUT_IMAGE_PATH = "/home/jay/BigData/MLProj732/dl/static/predimages/"

    def __init__(self, is_live=False):
        if is_live:
            self.INPUT_IMAGE_PATH = "/home/jay/BigData/MLProj732/dl/static/datalive/"

    def split_image(self, input_path, image_name, map_file_name, output_folder, extension, identifier):
        """
        Split sfu parking lot image
        :param input_path:
        :param image_name:
        :param map_file_name:
        :param output_folder:
        :param extension:
        :param identifier:
        :return:
        """
        img = Image.open(input_path + image_name + "." + extension)
        with open(map_file_name) as fp:
            count = 1
            for line in fp:
                coors = line.split(",")
                coors = (int(coors[0]), int(coors[1]), int(coors[2]), int(coors[3]))
                img.crop(coors).save(output_folder + identifier + str(count) + "." + extension)
                count += 1

    def split_all_sfu_images(self, actual_image_name, input_image_path, input_map_path, output_image_path, file_extension):
        # actual_image_name = actual_image_id + ".jpg"
        image_dir = output_image_path + str(actual_image_name) + "/"

        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        self.split_image(input_image_path, actual_image_name, input_map_path + "/L1.txt", image_dir, file_extension, "A_")
        self.split_image(input_image_path, actual_image_name, input_map_path + "/L2.txt", image_dir, file_extension, "B_")
        self.split_image(input_image_path, actual_image_name, input_map_path + "/L3.txt", image_dir, file_extension, "C_")

    @staticmethod
    def split_sfu_image(image_name,is_live=False):
        """
        Split SFU images
        :param image_name:
        :return:
        """

        imgspl = imagesplit(is_live)
        imgspl.split_all_sfu_images(image_name, imgspl.INPUT_IMAGE_PATH, imgspl.INPUT_MAP_PATH, imgspl.OUTPUT_IMAGE_PATH, 'jpg')
        return imgspl.OUTPUT_IMAGE_PATH + str(image_name) + "/"
