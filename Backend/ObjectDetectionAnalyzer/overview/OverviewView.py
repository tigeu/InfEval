from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.tasks.TasksModels import Tasks
from ObjectDetectionAnalyzer.upload.ModelTypes import ModelTypes
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Predictions, Models


class OverviewView(APIView):
    """
    Handle requests sent to /overview
    """

    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request):
        user = request.user

        response_data = {'datasets': self.get_datasets(user),
                         'predictions': self.get_predictions(user),
                         'models': self.get_models(user),
                         'tasks': self.get_tasks(user)}

        return Response(response_data, status=status.HTTP_200_OK)

    def get_datasets(self, user):
        datasets = Dataset.objects.filter(userId=user)
        response_datasets = []
        for dataset in datasets:
            data = {'name': dataset.name,
                    'groundTruth': True if dataset.ground_truth_path else False,
                    'predictions': True if Predictions.objects.filter(datasetId=dataset, userId=user) else False,
                    'uploaded': dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}

            response_datasets.append(data)
        return response_datasets

    def get_predictions(self, user):
        predictions = Predictions.objects.filter(userId=user)
        response_predictions = []
        for prediction in predictions:
            data = {'name': prediction.name,
                    'dataset': Dataset.objects.get(pk=prediction.datasetId.id).name,
                    'uploaded': prediction.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}

            response_predictions.append(data)
        return response_predictions

    def get_models(self, user):
        models = Models.objects.filter(userId=user)
        response_models = []
        for model in models:
            data = {'name': model.name,
                    'type': str(ModelTypes(model.type)),
                    'labelMap': True if model.label_map_path else False,
                    'uploaded': model.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}

            response_models.append(data)
        return response_models

    def get_tasks(self, user):
        tasks = Tasks.objects.filter(userId=user)
        response_tasks = []
        for task in tasks:
            data = {'name': task.name,
                    'description': task.description,
                    'progress': round(task.progress, 2),
                    'fileName': task.file_name,
                    'started': task.started.strftime('%Y-%m-%d %H:%M:%S'),
                    'finished': task.finished.strftime('%Y-%m-%d %H:%M:%S') if task.finished else "",
                    'dataset': Dataset.objects.get(pk=task.datasetId.id).name,
                    'model': Models.objects.get(pk=task.modelId.id).name
                    }

            response_tasks.append(data)
        return response_tasks
