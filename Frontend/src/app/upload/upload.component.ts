import {Component, Input, OnInit} from '@angular/core';
import {HttpErrorResponse, HttpEventType} from "@angular/common/http";
import {finalize, Subscription} from "rxjs";
import {UploadService} from "./upload.service";
import {UploadInformation} from "./UploadInformation";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";
import {DatasetFile} from "../dataset-list/dataset-file";
import {ModelFile} from "../model-list/model-file";
import {SelectedModelChangedService} from "../shared-services/selected-model-changed.service";

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent implements OnInit {
  @Input() uploadInformation!: UploadInformation;
  dataset: DatasetFile = {name: ''};
  model: ModelFile = {name: '', type: ''};

  file!: File | null;
  fileName: String = '';
  uploadProgress!: number | null;
  uploadSub!: Subscription | null;

  selectedDatasetChanged: Subscription;
  selectedModelChanged: Subscription;

  errorMessage: string = "";

  constructor(private uploadService: UploadService,
              private selectedDatasetChangedService: SelectedDatasetChangedService,
              private selectedModelChangedService: SelectedModelChangedService) {
    this.selectedDatasetChanged = this.selectedDatasetChangedService.newData.subscribe((data: DatasetFile) => {
      if (!this.uploadInformation.isDataset)
        this.dataset = data;
    })
    this.selectedModelChanged = this.selectedModelChangedService.newData.subscribe((data: ModelFile) => {
      if (!this.uploadInformation.isDataset && !this.uploadInformation.isModel)
        this.model = data;
    })
  }

  ngOnInit(): void {
  }

  ngOnDestroy(): void {
    this.selectedDatasetChanged.unsubscribe();
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (!file || (this.uploadInformation.uploadFileType && file.type !== this.uploadInformation.uploadFileType))
      return

    this.file = file
    this.fileName = file.name;
  }

  upload() {
    if (this.file && this.fileName) {
      this.errorMessage = "";
      this.uploadSub = this.uploadService.upload(this.fileName, this.file, this.dataset.name, this.model.name, this.uploadInformation.apiEndpoint)
        .pipe(finalize(() => this.reset()))
        .subscribe({
          next: (event) => {
            if (event.type == HttpEventType.UploadProgress) {
              this.updateProgress(event.loaded, event.total);
            }
          },
          error: this.setErrorMessage.bind(this)
        })
    }
  }

  updateProgress(loaded: number, total: number) {
    if (total)
      this.uploadProgress = Math.round(100 * (loaded / total));
  }

  cancelUpload() {
    if (this.uploadSub)
      this.uploadSub.unsubscribe();
    this.reset();
  }

  reset() {
    this.uploadProgress = null;
    this.uploadSub = null;
    this.file = null;
    this.fileName = '';
  }

  setDataset(value: string) {
    this.dataset = {name: value};
  }

  setModel(value: string) {
    this.model = {name: value, type: ''};
  }

  selectedModelTypeChanged(value: string) {
    this.uploadInformation.apiEndpoint = value;
  }

  setErrorMessage(res: HttpErrorResponse) {
    this.errorMessage = res.error;
  }
}
