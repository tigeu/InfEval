import {Component, OnInit} from '@angular/core';
import {UploadFileTypes} from "../upload/UploadFileTypes";
import {UploadInformation} from "../upload/UploadInformation";

@Component({
  selector: 'app-upload-main',
  templateUrl: './upload-main.component.html',
  styleUrls: ['./upload-main.component.css']
})
export class UploadMainComponent implements OnInit {
  /*
  Component that gets a list of predictions from /prediction-list and displays them in a dropdown menu. Selected
  prediction is sent to SelectedPredictionChangedService.

  Attributes
  ----------
  datasetInformation : UploadInformation
    Upload information for dataset
  groundTruthInformation : UploadInformation
    Upload information for ground truth
  labelMapInformation : UploadInformation
    Upload information for label map
  predictionsInformation : UploadInformation
    Upload information for predictions
  modelInformation : UploadInformation
    Upload information for model
  */
  datasetInformation: UploadInformation = {
    isDataset: true,
    isModel: false,
    uploadFileTypes: [UploadFileTypes.Zip, UploadFileTypes.XZip],
    uploadFileEnding: ".zip",
    apiEndpoint: "dataset"
  };
  groundTruthInformation: UploadInformation = {
    isDataset: false,
    isModel: false,
    uploadFileTypes: [UploadFileTypes.Csv],
    uploadFileEnding: ".csv",
    apiEndpoint: "ground-truth"
  };
  labelMapInformation: UploadInformation = {
    isDataset: false,
    isModel: false,
    uploadFileTypes: [UploadFileTypes.Text],
    uploadFileEnding: ".txt",
    apiEndpoint: "label-map"
  };
  predictionsInformation: UploadInformation = {
    isDataset: false,
    isModel: false,
    uploadFileTypes: [UploadFileTypes.Csv],
    uploadFileEnding: ".csv",
    apiEndpoint: "prediction"
  };
  modelInformation: UploadInformation = {
    isDataset: false,
    isModel: true,
    uploadFileTypes: [],
    uploadFileEnding: "*",
    apiEndpoint: ""
  };

  constructor() {
  }

  ngOnInit(): void {

  }
}
