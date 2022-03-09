from pathlib import Path

from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.services.CSVWriteService import CSVWriteService
from ObjectDetectionAnalyzer.services.JSONService import JSONService
from ObjectDetectionAnalyzer.services.PathService import PathService
from ObjectDetectionAnalyzer.services.PyTorchService import PyTorchService
from ObjectDetectionAnalyzer.services.TensorFlowService import TensorFlowService
from ObjectDetectionAnalyzer.services.YoloService import YoloService
from ObjectDetectionAnalyzer.settings import IMAGE_ENDINGS, YOLOV3_DIR, YOLOV5_DIR, DATA_DIR
from ObjectDetectionAnalyzer.tasks.TasksModels import Tasks
from ObjectDetectionAnalyzer.tasks.TasksService import TasksService
from ObjectDetectionAnalyzer.upload.ModelTypes import ModelTypes
from ObjectDetectionAnalyzer.upload.UploadModels import Models, Dataset, Predictions


class TasksView(APIView):
    """
    View that handles requests sent to /tasks.
    POST: Starts an inference task on a given dataset with a given model and writes its results into a prediction file

    Attributes
    ----------
    tasks_service : TasksService
        Service for executing task
    path_service : PathService
        Service for handling file system tasks
    tensor_flow_service : TensorFlowService
        Service for getting predictions from TensorFlowModel
    pytorch_service : PyTorchService
        Service for getting predictions from PyTorchModel
    yolo_service : YoloService
        Service for getting predictions from YoloModel
    json_service : JSONService
        Service for reading JSON (label map)
    csv_write_service : CSVWriteService
        Service for writing to CSV

    Methods
    -------
    post(request, task_name)
        Starts an inference task on a given dataset with a given model and writes its results into a prediction file
    _execute_task(dataset, desc, file_name, model, task_name, user)
        Execute actual inference task and save results
    _write_model_predictions(dataset, file_name, model_predictions, user)
        Write predictions to csv file
    _get_predictions(image_files, model, task)
        Get predictions from the given model
    """

    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        """
        Initialise required services
        """
        super().__init__(**kwargs)
        self.task_service = TasksService()
        self.path_service = PathService()
        self.tensor_flow_service = TensorFlowService()
        self.pytorch_service = PyTorchService()
        self.yolo_service = YoloService()
        self.json_service = JSONService()
        self.csv_write_service = CSVWriteService()

    def post(self, request, task_name):
        """
        Starts an inference task on a given dataset with a given model and writes its results into a prediction file

        Parameters
        ----------
        request : HttpRequest
            POST request
        task_name : str
            Name of the task that should be started

        Returns
        -------
        Response
            Success message with status code
        """
        user = request.user
        desc = request.data['task_description']
        file_name = request.data['file_name']
        dataset_name = request.data['dataset_name']
        model_name = request.data['model_name']

        if not file_name.endswith(".csv"):
            file_name = file_name + ".csv"

        dataset = Dataset.objects.filter(name=dataset_name, userId=user)
        if not dataset:
            return Response("Dataset does not exist yet", status=status.HTTP_404_NOT_FOUND)
        dataset = dataset.first()

        model = Models.objects.filter(name=model_name, userId=user)
        if not model:
            return Response("Model does not exist yet", status=status.HTTP_404_NOT_FOUND)
        model = model.first()

        task = Tasks.objects.filter(name=task_name, userId=user)
        if task and not task.first().finished:
            return Response("A task with this name is running already", status=status.HTTP_400_BAD_REQUEST)

        try:
            self._execute_task(dataset, desc, file_name, model, task_name, user)
        except AttributeError:
            return Response("Task has been deleted", status=status.HTTP_204_NO_CONTENT)
        except FileNotFoundError:
            return Response("Dataset has been deleted", status=status.HTTP_204_NO_CONTENT)

        return Response("Task finished successfully", status=status.HTTP_200_OK)

    def _execute_task(self, dataset, desc, file_name, model, task_name, user):
        """
        Execute actual inference task and save results

        Parameters
        ----------
        dataset : Dataset
            Name of given dataset
        desc : str
            Description of current task
        file_name : str
            Name of the prediction file
        model : Model
            Given model object
        task_name : str
            Name of current task
        user : user
            User that started the task
        """
        task = Tasks.objects.update_or_create(name=task_name, userId=user,
                                              defaults={'name': task_name, 'description': desc, 'file_name': file_name,
                                                        'progress': 0, 'userId': user, 'datasetId': dataset,
                                                        'modelId': model})[0]
        image_files = self.path_service.get_image_files_from_dir(Path(dataset.path), IMAGE_ENDINGS)
        model_predictions = self._get_predictions(image_files, model, task)
        if model_predictions is None:
            raise AttributeError()

        if model.label_map_path:
            label_map = self.json_service.read_label_map(model.label_map_path)
            self.task_service.replace_class_names(model_predictions, label_map)

        self._write_model_predictions(dataset, file_name, model_predictions, user)

        task.progress = 100
        task.finished = timezone.now()
        task.save()

    def _write_model_predictions(self, dataset, file_name, model_predictions, user):
        """
        Write predictions to csv file

        Parameters
        ----------
        dataset : Dataset
            Name of given dataset
        file_name : str
            Name of the prediction file
        model_predictions : list
            List of dictionaries, each representing a single prediction
        user : User
            User that started the task
        """
        user_dir = self.path_service.get_combined_dir(DATA_DIR, user.username)
        dataset_dir = self.path_service.get_dataset_dir(user_dir, dataset.name)
        predictions_dir = self.path_service.get_predictions_dir(dataset_dir)
        self.path_service.create_dir(predictions_dir)
        file_path = predictions_dir / file_name
        self.csv_write_service.write_predictions(model_predictions, file_path)
        Predictions.objects.update_or_create(name=file_name, path=file_path, datasetId=dataset, userId=user)

    def _get_predictions(self, image_files, model, task):
        """
        Get predictions from the given model

        Parameters
        ----------
        image_files : list
            List of paths of all image that should be predicted
        model : Model
            Given model object
        task : Task
            Current task

        Returns
        -------
        list
            List of dictionaries, each representing a single detection
        """
        if model.type == ModelTypes.TENSORFLOW1.value:
            detections = self.tensor_flow_service.get_detections_for_task_images(model.path, image_files, task, True)
        elif model.type == ModelTypes.TENSORFLOW2.value:
            detections = self.tensor_flow_service.get_detections_for_task_images(model.path, image_files, task)
        elif model.type == ModelTypes.PYTORCH.value:
            detections = self.pytorch_service.get_detections_for_task_images(model.path, image_files, task)
        elif model.type == ModelTypes.YOLOV3.value:
            detections = self.yolo_service.get_detections_for_task_images(YOLOV3_DIR, model.path, image_files, task)
        else:
            detections = self.yolo_service.get_detections_for_task_images(YOLOV5_DIR, model.path, image_files, task)
        return detections
