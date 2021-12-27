import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {UploadFileTypes} from "../upload/UploadFileTypes";
import {UploadInformation} from "../upload/UploadInformation";

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
    apiEndpoint: "predictions"
  };
  modelInformation: UploadInformation = {
    uploadFileType: UploadFileTypes.Binary,
    uploadFileEnding: ".pb",
    apiEndpoint: "model"
  };

  datasetName: string = "";

  datasetForm: FormGroup;

  constructor(private formBuilder: FormBuilder) {
    this.datasetForm = this.formBuilder.group({
      datasetName: ['', Validators.required],
    });
  }

  ngOnInit(): void {
  }

  datasetNameChange($event: any) {
    this.datasetName = this.datasetForm.value.datasetName;
  }
}
