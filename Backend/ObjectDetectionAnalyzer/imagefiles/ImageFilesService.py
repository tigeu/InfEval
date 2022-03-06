import os
from pathlib import Path


class ImageFilesService:
    """
    Service that contains a method for getting image file names.

    Methods
    -------
    get_image_file_names(directory, image_endings)
        Returns a list of image file names that have the correct ending
    """

    def get_image_file_names(self, directory, image_endings):
        """
        Returns a list of image file names that have the correct ending

        Parameters
        ----------
        directory : Path
            Path where the image file names should be retrieved
        image_endings : list
            List containing the wanted image endings

        Returns
        -------
        list
            List of image file names with correct ending
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
