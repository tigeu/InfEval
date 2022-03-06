import json


class JSONService:
    """
    Service that contains a method for reading a label map

    Methods
    -------
    read_label_map(file_path)
        Returns a dictionary containing the class numbers as keys and the class names as values
    """

    def read_label_map(self, file_path):
        """
        Reads a label map from given path and returns its content.

        Parameters
        ----------
        file_path : Path
            Path of the label map

        Returns
        -------
        dict
            Dictionary containing the class numbers as keys and the class names as values
        """
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        return data
