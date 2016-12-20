""" Problem specific image split, Scope of improvement and generalization"""
from PIL import Image
import os


class imagesplit:

    def split_image_by_map(self, image_path, map_file_name, output_folder, identifier):
        """
        Split parking lot image based on one map file
        :param image_path:
        :param map_file_name:
        :param output_folder:
        :param identifier:
        :return:
        """
        img = Image.open(image_path)
        basename = os.path.basename(image_path)
        filename, extension = os.path.splitext(basename)

        with open(map_file_name) as fp:
            count = 1
            for line in fp:
                coors = line.split(",")
                coors = (int(coors[0]), int(coors[1]), int(coors[2]), int(coors[3]))
                img.crop(coors).save(output_folder + identifier + str(count) + extension)
                count += 1

    def split_image(self, image_path, input_map_path, output_image_path):
        """
        Split images based on map file input
        :param image_path:
        :param input_map_path:
        :param output_image_path:
        :return:
        """
        basename = os.path.basename(image_path)
        filename, extension = os.path.splitext(basename)
        image_dir = output_image_path + filename + "/"

        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        self.split_image_by_map(image_path, input_map_path + "/L1.txt", image_dir, "A_")
        self.split_image_by_map(image_path, input_map_path + "/L2.txt", image_dir, "B_")
        self.split_image_by_map(image_path, input_map_path + "/L3.txt", image_dir, "C_")

        return image_dir
