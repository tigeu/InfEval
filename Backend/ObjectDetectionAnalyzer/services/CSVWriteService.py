import csv
import os


class CSVWriteService:
    def write_predictions(self, detections, file_path):
        with open(file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for image_path, detections in detections.items():
                image_name = base_name = os.path.basename(image_path)
                for detection in detections:
                    writer.writerow([image_name, detection['class'], detection['confidence'],
                                     detection['xmin'], detection['ymin'], detection['xmax'], detection['ymax']])
