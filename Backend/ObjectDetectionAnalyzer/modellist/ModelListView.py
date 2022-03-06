from pathlib import Path

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.modellist.ModelListSerializer import ModelListSerializer
from ObjectDetectionAnalyzer.services.PathService import PathService
from ObjectDetectionAnalyzer.upload.UploadModels import Models


class ModelListView(APIView):
    """
    View that handles requests sent to /model-list.
    GET: Returns a list of all models for the requesting user.
    DELETE: Delete a given model

    Attributes
    ----------
    path_service : PathService
        Service for handling file system tasks

    Methods
    -------
    get(request)
        Returns a list of all models for the requesting user
    delete(request, dataset)
        Delete a given model
    """

    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        """
        Initialise required services
        """
        super().__init__(**kwargs)
        self.path_service = PathService()

    def get(self, request):
        """
        Returns a list of all models for the requesting user

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

        models = Models.objects.filter(userId=user)

        response_data = []
        for model in models:
            data = {'name': model.name, 'type': model.type}
            response_data.append(data)

        serializer = ModelListSerializer(response_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, model):
        """
        Delete a given model

        Parameters
        ----------
        request : HttpRequest
            DELETE request
        model : str
            Name of model that should be deleted

        Returns
        -------
        Response
            Requested data with status code
        """
        user = request.user

        model = Models.objects.filter(userId=user, name=model).first()
        self.path_service.delete(Path(model.path))
        model.delete()

        return Response("Successfully deleted model", status=status.HTTP_200_OK)
