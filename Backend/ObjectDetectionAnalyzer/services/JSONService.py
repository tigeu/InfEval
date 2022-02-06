import json


class JSONService:
    def read_label_map(self, file_path):
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        return data
