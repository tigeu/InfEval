import csv


class CSVParseService:
    def get_values_for_image(self, file, image_name, indices):
        values = []
        with open(file, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
            for row in reader:
                file_name = row[indices['file_name']]
                if file_name == image_name:
                    values.append(self.get_value(row, indices))

            return values

    def get_value(self, row, indices):
        value = {'class': row[indices['class']],
                 'xmin': int(row[indices['xmin']]),
                 'ymin': int(row[indices['ymin']]),
                 'xmax': int(row[indices['xmax']]),
                 'ymax': int(row[indices['ymax']])}
        if 'confidence' in indices:
            value['confidence'] = round(float(row[indices['confidence']]) * 100)

        return value

    def get_classes(self, file, class_index):
        classes = set()
        with open(file, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
            for row in reader:
                classes.add(row[class_index])
            sorted_classes = sorted(list(classes))
            return sorted_classes
