import {Component, Input, OnInit} from '@angular/core';
import {HttpEventType} from "@angular/common/http";
import {finalize, Subscription} from "rxjs";
import {UploadService} from "./upload.service";
import {UploadInformation} from "./UploadInformation";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";
import {DatasetFile} from "../dataset-list/dataset-file";
import {ModelFile} from "../model-list/model-file";

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent implements OnInit {
  @Input() uploadInformation!: UploadInformation;
  dataset: DatasetFile = {name: ''};
  model: ModelFile = {name: ''};

  file!: File | null;
  fileName: String = '';
  uploadProgress!: number | null;
  uploadSub!: Subscription | null;

  selectedDatasetChanged: Subscription;

  constructor(private uploadService: UploadService,
              private selectedDatasetChangedService: SelectedDatasetChangedService) {
    this.selectedDatasetChanged = this.selectedDatasetChangedService.newData.subscribe((data: DatasetFile) => {
      if (!this.uploadInformation.isDataset)
        this.dataset = data;
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
      this.uploadSub = this.uploadService.upload(this.fileName, this.file, this.dataset.name, this.model.name, this.uploadInformation.apiEndpoint)
        .pipe(finalize(() => this.reset()))
        .subscribe(event => {
          if (event.type == HttpEventType.UploadProgress) {
            this.updateProgress(event.loaded, event.total);
          }
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
    this.model = {name: value};
  }

  selectedModelTypeChanged(value: string) {
    this.uploadInformation.apiEndpoint = value;
  }
}
