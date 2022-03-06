from pathlib import Path

from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.services.PathService import PathService
from ObjectDetectionAnalyzer.settings import TMP_DIR
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Models
from ObjectDetectionAnalyzer.upload.UploadService import UploadService


class UploadBaseView(APIView):
    """
    Base view for all upload views.
    PUT: Save uploaded file

    Attributes
    ----------
    path_service : PathService
        Service for handling file system tasks
    upload_service : UploadService
        Service for saving uploaded files

    Methods
    -------
    put(request)
        Save uploaded file
    requires_dataset()
        Returns True if dataset is required for current uploaded, False if dataset is not required
    requires_model()
        Returns True if model is required for current uploaded, False if model is not required
    is_file_valid(tmp_file_path)
        Returns True if current uploaded file is valid, False if the file is invalid
    get_target_dir(username, dataset_name, model_name)
        Returns directory in which the uploaded file should be saved
    create_dir(dir)
        Creates target directory and returns its success status
    save_data(tmp_file_path, target_dir, dataset_name, model_name, dataset, model, user, file_name)
        Save uploaded file in target directory
    """
    parser_classes = [MultiPartParser]

    def __init__(self, **kwargs):
        """
        Initialise required services
        """
        super().__init__(**kwargs)
        self.path_service = PathService()
        self.upload_service = UploadService()

    def put(self, request, file_name):
        """
        Save uploaded file

        Parameters
        ----------
        request : HttpRequest
            GET request
        file_name : str
            Name the file should be given when saved

        Returns
        -------
        Response
            Requested data with status code
        """
        user = request.user
        username = user.username
        file_obj = request.data['file']
        dataset_name = request.data['dataset_name']
        model_name = request.data['model_name']

        tmp_file_path = self.path_service.save_tmp_file(TMP_DIR, file_name, file_obj)
        if not tmp_file_path:
            return Response("File could not be saved", status=status.HTTP_400_BAD_REQUEST)

        dataset = Dataset.objects.filter(name=dataset_name, userId=user)
        if self.requires_dataset():
            if not dataset:
                self.path_service.delete_tmp_file(tmp_file_path)
                return Response("Dataset does not exist yet", status=status.HTTP_400_BAD_REQUEST)

        model = Models.objects.filter(name=model_name, userId=user)
        if self.requires_model():
            if not model:
                self.path_service.delete_tmp_file(tmp_file_path)
                return Response("Model does not exist yet", status=status.HTTP_400_BAD_REQUEST)

        if not self.is_file_valid(tmp_file_path):
            self.path_service.delete_tmp_file(tmp_file_path)
            return Response("Invalid file uploaded", status=status.HTTP_400_BAD_REQUEST)

        target_dir = self.get_target_dir(username, dataset_name, model_name)
        if not self.create_dir(target_dir):
            self.path_service.delete_tmp_file(tmp_file_path)
            return Response("Dataset directory could not be created", status=status.HTTP_400_BAD_REQUEST)

        self.save_data(tmp_file_path, target_dir, dataset_name, model_name, dataset, model, user, file_name)
        self.path_service.delete_tmp_file(tmp_file_path)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def requires_dataset(self):
        """
        Returns True if dataset is required for current uploaded, False if dataset is not required

        Returns
        -------
        bool
            Dataset required?
        """
        return True

    def requires_model(self):
        """
        Returns True if model is required for current uploaded, False if model is not required

        Returns
        -------
        bool
            Model required?
        """
        return False

    def is_file_valid(self, tmp_file_path):
        """
        Returns True if current uploaded file is valid, False if the file is invalid

        Parameters
        ----------
        tmp_file_path : Path
            Path of temporarily saved file

        Returns
        -------
        bool
            File valid?
        """
        pass

    def get_target_dir(self, username, dataset_name, model_name):
        """
        Returns directory in which the uploaded file should be saved

        Parameters
        ----------
        username : str
            Name of user who uploaded the file
        dataset_name : str
            Name of current dataset (if required)
        model_name : str
            Name of current model (if required)

        Returns
        -------
        Path
            Target directory where the file is saved
        """
        pass

    def create_dir(self, dir):
        """
        Creates target directory and returns its success status

        Parameters
        ----------
        dir : Path
            Target dir where the file should be saved

        Returns
        -------
        bool
            Indicates whether target directory could be created
        """
        return self.path_service.create_dir(dir, False)

    def save_data(self, tmp_file_path, target_dir, dataset_name, model_name, dataset, model, user, file_name):
        """
        Save uploaded file in target directory

        Parameters
        ----------
        tmp_file_path : Path
            Path where uploaded file is temporarily saved
        target_dir : Path
            Path where uploaded file should be saved
        dataset_name : str
            Name of current dataset (if required)
        model_name : str
            Name of current model (if required)
        dataset : Dataset
            Dataset object (if required)
        model : Model
            Model object (if required)
        user : User
            User who uploaded the file
        file_name : str
            Name the file should be given when saved
        """
        pass
