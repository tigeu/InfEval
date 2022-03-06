import csv
import os


class CSVWriteService:
    """
    Service that provides methods for writing predictions to a CSV file.

    Methods
    -------
    write_predictions(predictions, file_path)
        Writes given detections to a given CSV-file
    """

    def write_predictions(self, predictions, file_path):
        """
        Writes all predictions to a given file.

        Parameters
        ----------
        predictions : list
            List of dictionaries, each representing a row that should be written

        file_path : Path
            Path of the CSV-file that should be written
        """
        with open(file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for image_path, predictions in predictions.items():
                image_name = os.path.basename(image_path)
                for detection in predictions:
                    writer.writerow([image_name, detection['class'], detection['confidence'],
                                     detection['xmin'], detection['ymin'], detection['xmax'], detection['ymax']])
