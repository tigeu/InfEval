import {Component, OnInit} from '@angular/core';
import {UploadFileTypes} from "../upload/UploadFileTypes";
import {UploadInformation} from "../upload/UploadInformation";
import {debounceTime, distinctUntilChanged, Subject} from "rxjs";
import {DatasetFile} from "../dataset-list/dataset-file";

@Component({
  selector: 'app-upload-main',
  templateUrl: './upload-main.component.html',
  styleUrls: ['./upload-main.component.css']
})
export class UploadMainComponent implements OnInit {
  datasetInformation: UploadInformation = {
    uploadFileType: UploadFileTypes.Compressed,
    uploadFileEnding: ".zip",
    apiEndpoint: "dataset"
  };
  groundTruthInformation: UploadInformation = {
    uploadFileType: UploadFileTypes.Csv,
    uploadFileEnding: ".csv",
    apiEndpoint: "ground-truth"
  };
  labelMapInformation: UploadInformation = {
    uploadFileType: UploadFileTypes.Text,
    uploadFileEnding: ".txt",
    apiEndpoint: "label-map"
  };
  predictionsInformation: UploadInformation = {
    uploadFileType: UploadFileTypes.Csv,
    uploadFileEnding: ".csv",
    apiEndpoint: "prediction"
  };
  modelInformation: UploadInformation = {
    uploadFileType: UploadFileTypes.Binary,
    uploadFileEnding: ".pb",
    apiEndpoint: "model"
  };

  dataset: DatasetFile = {name: ""};
  datasetSubject = new Subject<DatasetFile>();

  constructor() {
  }

  ngOnInit(): void {
    this.datasetSubject.pipe(
      debounceTime(300),
      distinctUntilChanged()
    ).subscribe(dataset => {
      this.dataset = dataset;
    });
  }

  createDataset(datasetName: string) {
    this.datasetSubject.next({name: datasetName})
  }
}
