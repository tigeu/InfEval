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
    Handle requests sent to /tasks
    """

    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.task_service = TasksService()
        self.path_service = PathService()
        self.tensor_flow_service = TensorFlowService()
        self.pytorch_service = PyTorchService()
        self.yolo_service = YoloService()
        self.json_service = JSONService()
        self.csv_write_service = CSVWriteService()

    def post(self, request, task_name):
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
        if task:
            return Response("A task with this name is running already", status=status.HTTP_400_BAD_REQUEST)

        self.execute_task(dataset, desc, file_name, model, task_name, user)

        return Response("Task finished successfully", status=status.HTTP_200_OK)

    def execute_task(self, dataset, desc, file_name, model, task_name, user):
        task = Tasks.objects.update_or_create(name=task_name, userId=user,
                                              defaults={'name': task_name, 'description': desc, 'file_name': file_name,
                                                        'progress': 0, 'userId': user, 'datasetId': dataset,
                                                        'modelId': model})[0]
        image_files = self.path_service.get_image_files_from_dir(dataset.path, IMAGE_ENDINGS)
        model_predictions = self.get_detections(image_files, model, task)

        if model.label_map_path:
            label_map = self.json_service.read_label_map(model.label_map_path)
            self.task_service.replace_class_names(model_predictions, label_map)

        self.write_model_predictions(dataset, file_name, model_predictions, user)

        task.progress = 100
        task.finished = timezone.now()
        task.save()

    def write_model_predictions(self, dataset, file_name, model_predictions, user):
        user_dir = self.path_service.get_combined_dir(DATA_DIR, user.username)
        dataset_dir = self.path_service.get_dataset_dir(user_dir, dataset.name)
        predictions_dir = self.path_service.get_predictions_dir(dataset_dir)
        self.path_service.create_dir(predictions_dir)
        file_path = predictions_dir / file_name
        self.csv_write_service.write_predictions(model_predictions, file_path)
        Predictions.objects.update_or_create(name=file_name, path=file_path, datasetId=dataset, userId=user)

    def get_detections(self, image_files, model, task):
        if model.type == str(ModelTypes.TENSORFLOW1):
            detections = self.tensor_flow_service.get_detections_for_task_images(model.path, image_files, task, True)
        elif model.type == str(ModelTypes.TENSORFLOW2):
            detections = self.tensor_flow_service.get_detections_for_task_images(model.path, image_files, task)
        elif model.type == str(ModelTypes.PYTORCH):
            detections = self.pytorch_service.get_detections_for_task_images(model.path, image_files, task)
        elif model.type == str(ModelTypes.YOLOV3):
            detections = self.yolo_service.get_detections_for_task_images(YOLOV3_DIR, model.path, image_files, task)
        else:
            detections = self.yolo_service.get_detections_for_task_images(YOLOV5_DIR, model.path, image_files, task)
        return detections
