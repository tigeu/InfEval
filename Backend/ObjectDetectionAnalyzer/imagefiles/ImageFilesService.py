import os
from pathlib import Path


class ImageFilesService:
    """
    Service for getting image file names
    """

    def get_image_file_names(self, directory: Path, image_endings: dict) -> list:
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
