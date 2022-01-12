import csv


class CSVParseService:
    def get_ground_truth_values(self, file, image_name):
        predictions = []
        with open(file, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
            for row in reader:
                file_name = row[0]
                if not file_name == image_name:
                    continue
                predictions.append(
                    {'class': row[1],
                     'xmin': int(row[2]), 'ymin': int(row[3]), 'xmax': int(row[4]), 'ymax': int(row[5])}
                )
            return predictions

    def get_ground_truth_classes(self, file):
        classes = set()
        with open(file, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
            for row in reader:
                classes.add(row[1])
            sorted_classes = sorted(list(classes))
            classes_dict = {sorted_class: index for index, sorted_class in enumerate(sorted_classes)}
            return classes_dict
