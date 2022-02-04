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
    uploadFileType: UploadFileTypes.Compressed,
    uploadFileEnding: ".zip",
    apiEndpoint: "dataset"
  };
  groundTruthInformation: UploadInformation = {
    isDataset: false,
    isModel: false,
    uploadFileType: UploadFileTypes.Csv,
    uploadFileEnding: ".csv",
    apiEndpoint: "ground-truth"
  };
  labelMapInformation: UploadInformation = {
    isDataset: false,
    isModel: false,
    uploadFileType: UploadFileTypes.Text,
    uploadFileEnding: ".txt",
    apiEndpoint: "label-map"
  };
  predictionsInformation: UploadInformation = {
    isDataset: false,
    isModel: false,
    uploadFileType: UploadFileTypes.Csv,
    uploadFileEnding: ".csv",
    apiEndpoint: "prediction"
  };
  modelInformation: UploadInformation = {
    isDataset: false,
    isModel: true,
    uploadFileType: UploadFileTypes.Binary,
    uploadFileEnding: ".pt",
    apiEndpoint: "pytorch"
  };

  constructor() {
  }

  ngOnInit(): void {

  }
}
