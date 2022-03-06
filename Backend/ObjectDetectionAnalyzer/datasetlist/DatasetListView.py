from pathlib import Path

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ObjectDetectionAnalyzer.datasetlist.DatasetListSerializer import DatasetListSerializer
from ObjectDetectionAnalyzer.services.CSVParseService import CSVParseService
from ObjectDetectionAnalyzer.services.ColorService import ColorService
from ObjectDetectionAnalyzer.services.PathService import PathService
from ObjectDetectionAnalyzer.settings import GROUND_TRUTH_INDICES
from ObjectDetectionAnalyzer.upload.UploadModels import Dataset, Predictions


class DatasetListView(APIView):
    """
    View that handles requests sent to /dataset-list.
    GET: Returns a list of all datasets for the requesting user together with other information such as availability of
         ground truth, predictions and classes contained.
    DELETE: Delete a given dataset, together with all data and files related to it

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
        Returns a list of all datasets for the requesting user together with other information such as availability of
        ground truth, predictions and classes contained
    delete(request, dataset)
        Delete a given dataset, together with all data and files related to it
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

    def get(self, request):
        """
        Returns a list of all datasets for the requesting user together with other information such as availability of
        ground truth, predictions and classes contained

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

        datasets = Dataset.objects.filter(userId=user)

        response_data = []
        for dataset in datasets:
            data = {'name': dataset.name}
            if dataset.ground_truth_path:
                data['ground_truth'] = True
                classes = self.csv_parse_service.get_classes(dataset.ground_truth_path, GROUND_TRUTH_INDICES['class'])
                data['classes'] = classes
                data['colors'] = self.color_service.get_class_colors(classes)
            else:
                data['ground_truth'] = False
                data['classes'] = []
                data['colors'] = []
            predictions = Predictions.objects.filter(datasetId=dataset, userId=user)
            if predictions:
                data['predictions'] = True
            else:
                data['predictions'] = False
            response_data.append(data)

        serializer = DatasetListSerializer(response_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, dataset):
        """
        Delete a given dataset, together with all data and files related to it

        Parameters
        ----------
        request : HttpRequest
            DELETE request
        dataset : str
            Name of dataset that should be deleted

        Returns
        -------
        Response
            Requested data with status code
        """
        user = request.user

        dataset = Dataset.objects.filter(name=dataset, userId=user).first()
        self.path_service.delete(Path(dataset.path))
        dataset.delete()

        return Response("Successfully deleted dataset", status=status.HTTP_200_OK)
