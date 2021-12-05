import base64
import os


class FileService:
    """
    Service for retrieving files from os
    """

    def get_image_file_names(self, directory, image_endings):
        """
        Get file names of images with specific endings in a certain directory
        """
        if not os.path.exists(directory):
            return None

        all_file_names = os.listdir(directory)
        image_names = []
        for file_name in all_file_names:
            base_name = os.path.basename(file_name)
            extension = os.path.splitext(file_name)[1]
            if extension.lower() in image_endings:
                image_names.append(base_name)

        return image_names

    def encode_image(self, image_name):
        """
        Open image and encode it in base64
        """
        if not os.path.exists(image_name):
            return None

        with open(image_name, mode='rb') as file:
            image_base64 = base64.b64encode(file.read()).decode('utf-8')

        return image_base64
