from pathlib import Path

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.predictionlist.PredictionListSerializer import PredictionListSerializer
from ObjectDetectionAnalyzer.services.CSVParseService import CSVParseService
from ObjectDetectionAnalyzer.services.ColorService import ColorService
from ObjectDetectionAnalyzer.services.PathService import PathService
from ObjectDetectionAnalyzer.settings import PREDICTION_INDICES
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Predictions


class PredictionListView(APIView):
    """
    View that handles requests sent to /prediction-list.
    GET: Returns a list of all prediction files for the requesting user together with other information such as
         contained classes.
    DELETE: Delete a given prediction file, together with all data related to it

    Attributes
    ----------
    csv_path_service : CSVParseService
        Service for parsing CSV-files
    color_service : ColorService
        Service for getting colors for drawing bounding boxs
    path_service : PathService
        Service for handling file system tasks

    Methods
    -------
    get(request)
        Returns a list of all prediction files for the requesting user together with other information such as
        contained classes.
    delete(request, dataset)
        Delete a given prediction file, together with all data related to it
    """

    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        """
        Initialise required services
        """
        super().__init__(**kwargs)
        self.csv_parse_service = CSVParseService()
        self.color_service = ColorService()
        self.path_service = PathService()

    def get(self, request, dataset):
        """
        Returns a list of all prediction files for the requesting user together with other information such as
        contained classes.

        Parameters
        ----------
        request : HttpRequest
            GET request
        dataset : str
            Name of dataset

        Returns
        -------
        Response
            Requested data with status code
        """
        user = request.user

        filtered_dataset = Dataset.objects.filter(name=dataset, userId=user)
        if not filtered_dataset:
            return Response("Dataset does not exist yet", status=status.HTTP_404_NOT_FOUND)

        predictions = Predictions.objects.filter(datasetId=filtered_dataset.first(), userId=user)
        if not predictions:
            return Response("No predictions available for this dataset yet", status=status.HTTP_404_NOT_FOUND)

        response_data = []
        for prediction in predictions:
            classes = self.csv_parse_service.get_classes(prediction.path, PREDICTION_INDICES['class'])
            data = {'name': prediction.name, 'classes': classes, 'colors': self.color_service.get_class_colors(classes)}

            response_data.append(data)

        serializer = PredictionListSerializer(response_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, dataset):  # actually prediction name, but needs to be named dataset because of get
        """
        Delete a given prediction file, together with all data related to it

        Parameters
        ----------
        request : HttpRequest
            GET request
        dataset : str
            Name of prediction

        Returns
        -------
        Response
            Requested data with status code
        """
        prediction = dataset
        user = request.user

        prediction = Predictions.objects.filter(userId=user, name=prediction).first()
        self.path_service.delete(Path(prediction.path))
        prediction.delete()

        return Response("Successfully deleted prediction", status=status.HTTP_200_OK)
