import {Component, Input, OnInit, SimpleChanges} from '@angular/core';
import {HttpEventType} from "@angular/common/http";
import {finalize, Subscription} from "rxjs";
import {UploadService} from "./upload.service";
import {UploadInformation} from "./UploadInformation";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent implements OnInit {
  @Input() uploadInformation!: UploadInformation;
  @Input() datasetName!: string;

  file!: File | null;
  fileName: String = '';
  uploadProgress!: number | null;
  uploadSub!: Subscription | null;

  selectedDatasetChanged: Subscription;

  constructor(private uploadService: UploadService,
              private selectedDatasetChangedService: SelectedDatasetChangedService) {
    this.selectedDatasetChanged = this.selectedDatasetChangedService.newData.subscribe((data: string) => {
      this.datasetName = data;
    })
  }

  ngOnInit(): void {
  }

  ngOnChanges(changes: SimpleChanges) {
    if ("datasetName" in changes)
      this.datasetName = changes["datasetName"].currentValue;
  }

  onFileSelected(event: any) {
    this.file = event.target.files[0];
    if (!this.file || this.file.type !== this.uploadInformation.uploadFileType)
      return

    this.fileName = this.file.name;
  }

  upload() {
    if (this.file) {
      this.uploadSub = this.uploadService.upload(this.fileName, this.file, this.datasetName, this.uploadInformation.apiEndpoint)
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
}
