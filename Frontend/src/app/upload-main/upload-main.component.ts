import {Component, OnInit} from '@angular/core';
import {UploadFileTypes} from "../upload/UploadFileTypes";
import {UploadInformation} from "../upload/UploadInformation";

@Component({
  selector: 'app-upload-main',
  templateUrl: './upload-main.component.html',
  styleUrls: ['./upload-main.component.css']
})
export class UploadMainComponent implements OnInit {
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
    uploadFileTypes: [UploadFileTypes.Binary],
    uploadFileEnding: "*",
    apiEndpoint: ""
  };

  constructor() {
  }

  ngOnInit(): void {

  }
}
