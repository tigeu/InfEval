import csv


class CSVParseService:
    """
    Service that provides methods for reading data from a CSV file for detections or ground truth values of different
    structures. An "indices" dictionary needs to be given which has to contain at least file_name, class, xmin, ymin,
    xmax, ymax. For detections, confidence is also necessary.

    Methods
    -------
    get_values(file, indices)
        Returns a list of dictionaries, each presenting a read line from the file. All values are parsed.

    get_values_for_image(file, image_name, indices)
        Returns a list of dictionaries, each presenting a read line from the file for the given image.

    get_classes(file, class_index):
        Returns a list of all classes that can be found in the file

    _get_value(row, indices)
        Returns a parsed value of a row in form of a dictionary.
    """

    def get_values(self, file, indices):
        """
        Reads all values from a given file by extracting the data using the given indices, which indicate which
        attribute can be found at which index in the row.

        Parameters
        ----------
        file : file
            CSV-file that should be parsed
        indices : dict
            Dictionary containing at least file_name, class, xmin, ymin, xmax, ymax. For detections, confidence is also
            necessary

        Returns
        -------
        list
            List of dictionaries, each one presenting a single parsed row
        """
        values = []
        with open(file, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
            for row in reader:
                values.append(self._get_value(row, indices))

            return values

    def get_values_for_image(self, file, image_name, indices):
        """
        Reads all values from a given file for a given image by extracting the data using the given indices, which
        indicate which  attribute can be found at which index in the row.

        Parameters
        ----------
        file : file
            CSV-file that should be parsed
        image_name : str
            Name of the image whose values should be parsed from the file
        indices : dict
            Dictionary containing at least file_name, class, xmin, ymin, xmax, ymax. For detections, confidence is also
            necessary

        Returns
        -------
        list
            List of dictionaries, each one presenting a single parsed row
        """
        values = []
        with open(file, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
            for row in reader:
                file_name = row[indices['file_name']]
                if file_name == image_name:
                    values.append(self._get_value(row, indices))

            return values

    def get_classes(self, file, class_index):
        """
        Reads all classes from a given CSV file.

        Parameters
        ----------
        file : file
            CSV-file that should be parsed
        class_index : int
            Index where the class_name can be found in each row

        Returns
        -------
        list
            List of strings with all unique class names
        """
        classes = set()
        with open(file, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
            for row in reader:
                classes.add(row[class_index])
            sorted_classes = sorted(list(classes))
            return sorted_classes

    def _get_value(self, row, indices):
        """
        Parses a single row using the given indices.

        Parameters
        ----------
        row : Row
            Row from CSVReader
        indices : dict
            Dictionary containing at least file_name, class, xmin, ymin, xmax, ymax. For detections, confidence is also
            necessary

        Returns
        -------
        dict
            Dictionary representing a single parsed row
        """
        value = {'class': row[indices['class']],
                 'file_name': row[indices['file_name']],
                 'xmin': int(float(row[indices['xmin']])),
                 'ymin': int(float(row[indices['ymin']])),
                 'xmax': int(float(row[indices['xmax']])),
                 'ymax': int(float(row[indices['ymax']]))}
        if 'confidence' in indices:
            value['confidence'] = round(float(row[indices['confidence']]) * 100)

        return value
