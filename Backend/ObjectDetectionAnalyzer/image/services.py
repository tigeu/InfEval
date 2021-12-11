import base64
import os


class ImageService:
    """
    Service for encoding images
    """

    def encode_image(self, image_name):
        """
        Open image and encode it in base64
        """
        if not os.path.exists(image_name):
            return None

        with open(image_name, mode='rb') as file:
            image_base64 = base64.b64encode(file.read()).decode('utf-8')

        return image_base64
