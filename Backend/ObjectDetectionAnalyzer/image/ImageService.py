import base64
import os


class ImageService:
    """
    Service that contains a method for encoding an image in base64

    Methods
    -------
    encode_image(image_name)
        Encodes the given image in base64
    """

    def encode_image(self, image_name):
        """
        Encodes the given image in base64

        Parameters
        ----------
        image_name : str
            Image that should be encoded

        Returns
        -------
        str
            Base64 encoded image or None if no image_name given
        """
        if not os.path.exists(image_name):
            return None

        with open(image_name, mode='rb') as file:
            image_base64 = base64.b64encode(file.read()).decode('utf-8')

        return image_base64
