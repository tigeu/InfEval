from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.tasks.TasksModels import Tasks
from ObjectDetectionAnalyzer.taskslist.TasksListSerializer import TasksListSerializer
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Models


class TasksListView(APIView):
    """
    Handle requests sent to /tasks-list
    """

    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request):
        user = request.user

        tasks = list(Tasks.objects.filter(userId=user))
        tasks.sort(key=lambda x: x.started, reverse=True)

        response_data = []
        for task in tasks:
            data = {'name': task.name,
                    'description': task.description,
                    'fileName': task.file_name,
                    'progress': round(task.progress, 2),
                    'started': task.started.strftime('%Y-%m-%d %H:%M:%S'),
                    'finished': task.finished.strftime('%Y-%m-%d %H:%M:%S') if task.finished else "",
                    'dataset': Dataset.objects.get(pk=task.datasetId.id).name,
                    'model': Models.objects.get(pk=task.modelId.id).name
                    }
            response_data.append(data)

        serializer = TasksListSerializer(response_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
