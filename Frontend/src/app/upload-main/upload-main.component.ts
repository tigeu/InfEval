import {Component, OnInit} from '@angular/core';
import {UploadFileTypes} from "../upload/UploadFileTypes";
import {UploadInformation} from "../upload/UploadInformation";
import {debounceTime, distinctUntilChanged, Subject} from "rxjs";

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

    datasetName: string = "";

    datasetNameSubject = new Subject<string>();

    constructor() {
    }

    ngOnInit(): void {
        this.datasetNameSubject.pipe(
            debounceTime(300),
            distinctUntilChanged()
        ).subscribe(name => {
            this.datasetName = name;
        });
    }

    setDatasetName(datasetName: string) {
        this.datasetNameSubject.next(datasetName)
    }
}
