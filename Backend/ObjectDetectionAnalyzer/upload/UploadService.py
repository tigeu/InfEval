import os
import shutil
import zipfile
from pathlib import Path

from PIL import Image

from ObjectDetectionAnalyzer.upload.validators.GroundTruthValidator import GroundTruthValidator
from ObjectDetectionAnalyzer.upload.validators.LabelMapValidator import LabelMapValidator
from ObjectDetectionAnalyzer.upload.validators.PredictionsValidator import PredictionsValidator
from ObjectDetectionAnalyzer.upload.validators.PyTorchValidator import PyTorchValidator
from ObjectDetectionAnalyzer.upload.validators.TensorFlowValidator import TensorFlowValidator
from ObjectDetectionAnalyzer.upload.validators.YoloValidator import YoloValidator


class UploadService:
    """
    Service that contains methods for validating files and saving data.

    Methods
    -------
    is_zip_valid(tmp_file_path, image_endings)
        Returns True if given zip is valid, False if zip is invalid
    is_ground_truth_valid(tmp_file_path)
        Returns the read values if file is valid, an empty list if the file is not valid.
    is_label_map_valid(tmp_file_path)
        Returns true if given txt label map file is valid, False if file is invalid
    is_prediction_valid(tmp_file_path)
        Returns True if given csv prediction file is valid, False if file is invalid
    is_pytorch_valid(tmp_file_path)
        Returns True if given PyTorch model is valid, False if file is invalid
    is_tf_valid(tmp_file_path, tmp_dir, is_tensor_flow_1=False)
        Returns True if given TensorFlow model is valid, False if file is invalid
    is_yolo_valid(tmp_file_path, yolo_dir)
        Returns True if given Yolo model is valid, False if file is invalid
    save_compressed_data(tmp_file_path, dataset_dir, image_endings)
        Save data from a zip file in dataset directory
    save_compressed_model(tmp_file_path, model_dir, model_name)
        Save model from a zip file in the model directory under the given model name
    save_data(tmp_file_path, target_dir, file_name)
        Save any file in target directory under given file name
    has_invalid_bounding_boxes(self, values, images)
        Checks if all bounding boxes are inside of the image boundaries
    """

    def is_zip_valid(self, tmp_file_path: Path, image_endings: set) -> bool:
        """
        Returns True if given zip is valid, False if zip is invalid

        Parameters
        ----------
        tmp_file_path : Path
            Path of temporarily saved file
        image_endings : list
            List of image endings that should be considered

        Returns
        -------
        bool
            Indicates whether zip is valid
        """
        contains_image = False
        if not zipfile.is_zipfile(tmp_file_path):
            return False

        with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                _, ext = os.path.splitext(file)
                if ext.lower() in image_endings:
                    contains_image = True
                    break
        return contains_image

    def is_ground_truth_valid(self, tmp_file_path):
        """
        Returns the read values if file is valid, an empty list if the file is not valid.

        Parameters
        ----------
        tmp_file_path : Path
            Path of temporarily saved file

        Returns
        -------
        list
            List with valid values. List is empty if file is invalid.
        """
        return GroundTruthValidator().is_valid(tmp_file_path)

    def is_label_map_valid(self, tmp_file_path):
        """
        Returns true if given txt label map file is valid, False if file is invalid

        Parameters
        ----------
        tmp_file_path : Path
            Path of temporarily saved file

        Returns
        -------
        bool
            Indicates whether label map is valid
        """
        return LabelMapValidator().is_valid(tmp_file_path)

    def is_prediction_valid(self, tmp_file_path):
        """
        Returns True if given csv prediction file is valid, False if file is invalid

        Parameters
        ----------
        tmp_file_path : Path
            Path of temporarily saved file

        Returns
        -------
        bool
            Indicates whether prediction is valid
        """
        return PredictionsValidator().is_valid(tmp_file_path)

    def is_pytorch_valid(self, tmp_file_path):
        """
        Returns True if given PyTorch model is valid, False if file is invalid

        Parameters
        ----------
        tmp_file_path : Path
            Path of temporarily saved file

        Returns
        -------
        bool
            Indicates whether model is valid
        """
        return PyTorchValidator().is_valid(tmp_file_path)

    def is_tf_valid(self, tmp_file_path, tmp_dir, is_tensor_flow_1=False):
        """
        Returns True if given TensorFlow model is valid, False if file is invalid

        Parameters
        ----------
        tmp_file_path : Path
            Path of temporarily saved file
        tmp_dir : Path
            Path of temporarily saved files
        is_tensor_flow_1 : bool
            Indicates whether model is TensorFlow1 or TensorFlow2

        Returns
        -------
        bool
            Indicates whether model is valid
        """
        if not zipfile.is_zipfile(tmp_file_path):
            return False

        dir = self.save_compressed_model(tmp_file_path, tmp_dir, "")
        if not dir:
            return False

        is_valid = TensorFlowValidator().is_valid(dir, is_tensor_flow_1)
        shutil.rmtree(dir)

        return is_valid

    def is_yolo_valid(self, tmp_file_path, yolo_dir):
        """
        Returns True if given Yolo model is valid, False if file is invalid

        Parameters
        ----------
        tmp_file_path : Path
            Path of temporarily saved file
        yolo_dir : Path
            Path of yolo directory which should be used for inference

        Returns
        -------
        bool
            Indicates whether model is valid
        """
        return YoloValidator().is_valid(tmp_file_path, yolo_dir)

    def save_compressed_data(self, tmp_file_path, dataset_dir, image_endings):
        """
        Save data from a zip file in dataset directory

        Parameters
        ----------
        tmp_file_path : Path
            Path of temporarily saved file
        dataset_dir : Path
            Path of dataset directory where zip content should be saved
        image_endings : list
            List of image endings that should be saved
        """
        with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                _, ext = os.path.splitext(member)
                if ext.lower() not in image_endings or member.startswith('.'):
                    continue  # skip non-image files and hidden images files
                filename = os.path.basename(member)
                source = zip_ref.open(member)
                target = open(os.path.join(dataset_dir, filename), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)

    def save_compressed_model(self, tmp_file_path, model_dir, model_name):
        """
        Save model from a zip file in the model directory under the given model name

        Parameters
        ----------
        tmp_file_path : Path
            Path of temporarily saved file
        model_dir : Path
            Path of model directory where model should be saved
        model_name : str
            Name under which the model should be saved

        Returns
        -------
        Path
            Path of the saved model in model directory or an empty string if "saved_model" was not found
        """
        extracted = False
        target_path = Path(os.path.join(model_dir, model_name))
        if target_path.exists() and not target_path.is_dir():
            Path.unlink(target_path)

        with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if 'saved_model/' in file:
                    extracted = True
                    zip_ref.extract(file, target_path)

        if extracted:
            return os.path.join(target_path, "saved_model/")

        return ""

    def save_data(self, tmp_file_path, target_dir, file_name):
        """
        Save any file in target directory under given file name

        Parameters
        ----------
        tmp_file_path : Path
            Path of temporarily saved file
        target_dir : Path
            Path of target directory where file should be saved
        file_name : str
            Name under which the file should be saved

        Returns
        -------
        Path
            Path of the saved file in target directory
        """
        path = target_dir / file_name
        shutil.copy(tmp_file_path, path)

        return path

    def has_invalid_bounding_boxes(self, values, images):
        """
        Checks if all bounding boxes are inside of the image boundaries

        Parameters
        ----------
        values : list
            List of dictionaries, each representing a ground truth value or prediction
        images : list
            List of full paths of the dataset images

        Returns
        -------
        bool
            Indicator whether there were invalid bounding boxes
        """
        for image in images:
            image_name = os.path.basename(image)
            image_values = filter(lambda x: x['file_name'] == image_name, values)
            width, height = Image.open(image).size
            for value in image_values:
                if value['xmin'] < 0 or value['ymin'] < 0 or value['xmax'] > width or value['ymax'] > height:
                    return False

        return True
