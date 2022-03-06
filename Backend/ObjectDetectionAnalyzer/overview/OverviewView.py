from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.tasks.TasksModels import Tasks
from ObjectDetectionAnalyzer.upload.ModelTypes import ModelTypes
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Predictions, Models


class OverviewView(APIView):
    """
    View that handles requests sent to /overview.
    GET: Returns a dictionary containing all user-specific data (datasets, predictions, models, tasks)

    Methods
    -------
    get(request)
        Returns a dictionary containing all user-specific data (datasets, predictions, models, tasks)
    get_datasets(user)
        Get all uploaded datasets for a specific user
    get_predictions(user)
        Get all uploaded prediction files for a specific user
    get_models(user)
        Get all uploaded models for a specific user
    get_tasks(user)
        Get all uploaded tasks for a specific user
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns a dictionary containing all user-specific data (datasets, predictions, models, tasks)

        Parameters
        ----------
        request : HttpRequest
            GET request

        Returns
        -------
        Response
            Requested data with status code
        """
        user = request.user

        response_data = {'datasets': self.get_datasets(user),
                         'predictions': self.get_predictions(user),
                         'models': self.get_models(user),
                         'tasks': self.get_tasks(user)}

        return Response(response_data, status=status.HTTP_200_OK)

    def get_datasets(self, user):
        """
        Get all uploaded datasets for a specific user

        Parameters
        ----------
        user : User
            User that sent the GET request

        Returns
        -------
        list
            List of dictionaries, each representing a single dataset
        """
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
        """
        Get all uploaded prediction files for a specific user

        Parameters
        ----------
        user : User
            User that sent the GET request

        Returns
        -------
        list
            List of dictionaries, each representing a single prediction file
        """
        predictions = Predictions.objects.filter(userId=user)
        response_predictions = []
        for prediction in predictions:
            data = {'name': prediction.name,
                    'dataset': Dataset.objects.get(pk=prediction.datasetId.id).name,
                    'uploaded': prediction.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}

            response_predictions.append(data)
        return response_predictions

    def get_models(self, user):
        """
        Get all uploaded models for a specific user

        Parameters
        ----------
        user : User
            User that sent the GET request

        Returns
        -------
        list
            List of dictionaries, each representing a single model
        """
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
        """
        Get all uploaded tasks for a specific user

        Parameters
        ----------
        user : User
            User that sent the GET request

        Returns
        -------
        list
            List of dictionaries, each representing a single task
        """
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
