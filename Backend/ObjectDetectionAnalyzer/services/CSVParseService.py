import csv


class CSVParseService:
    def get_values(self, file, indices):
        values = {}
        with open(file, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
            for row in reader:
                file_name = row[indices['file_name']]
                if file_name not in values:
                    values[file_name] = []
                values[file_name].append(self.get_value(row, indices))

            return values

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
                 'xmin': int(float(row[indices['xmin']])),
                 'ymin': int(float(row[indices['ymin']])),
                 'xmax': int(float(row[indices['xmax']])),
                 'ymax': int(float(row[indices['ymax']]))}
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
