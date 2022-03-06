from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.tasks.TasksModels import Tasks
from ObjectDetectionAnalyzer.taskslist.TasksListSerializer import TasksListSerializer
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Models


class TasksListView(APIView):
    """
    View that handles requests sent to /tasks-list.
    GET: Returns a list of all tasks for the requesting user.
    DELETE: Delete a given task, together with all data related to it

    Methods
    -------
    get(request)
        Returns a list of all tasks for the requesting user.
    delete(request, dataset)
        Delete a given task, together with all data related to it
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns a list of all tasks for the requesting user.

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

    def delete(self, request, task):
        """
        Delete a given task, together with all data related to it

        Parameters
        ----------
        request : HttpRequest
            DELETE request
        task : str
            Name of task that should be deleted

        Returns
        -------
        Response
            Success message with status code
        """
        user = request.user

        task = Tasks.objects.filter(userId=user, name=task).first()
        task.delete()

        return Response("Successfully deleted task", status=status.HTTP_200_OK)
