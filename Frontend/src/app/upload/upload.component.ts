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
  /*
  Component for uploading different files. Individual specifications can be found in uploadInformation.

  Attributes
  ----------
  uploadService : UploadService
    Service for uploading files
  selectedDatasetChangedService : SelectedDatasetChangedService
    Service for retrieving the selected dataset from a shared service
  selectedModelChangedService : SelectedModelChangedService
    Service for retrieving the selected model from a shared service
  uploadInformation : UploadInformation
    Important information for uploaded file type
  dataset : DatasetFile
    Currently selected dataset
  model : ModelFile
    Currently selected model
  file : File
    Uploaded file
  fileName : String
    Name of uploaded file
  uploadProgress : number
    Progress of current uplaod in percentage
  selectedDatasetChanged : Subscription
    Subscription for retrieving the selected dataset from a shared service
  selectedMdelChanged : Subscription
    Service for retrieving the selected model from a shared service
  errorMessage : string
    Error message from upload
  successMessage : string
    Success message from upload

  Methods
  -------
  onFileSelected(event: any)
    Save selected file if the type is correct
  upload(prediction: string)
    Upload file to backend and track progress
  updateProgress(loaded: number, total: number)
    Update progress for current upload
  cancelUpload()
    Cancel current upload
  reset()
    Reset current upload and file
  setDataset(value: string)
    Set current dataset
  setModel(value: string)
    Set current model
  selectedModelTypeChanged(value: string)
    Change selected model type (TF2, PyTorch, YOLOv3, YOLOv5)
  setErrorMessage(res: HttpErrorResponse)
    Set error message and remove success message
  */
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
  successMessage: string = ""

  constructor(private uploadService: UploadService,
              private selectedDatasetChangedService: SelectedDatasetChangedService,
              private selectedModelChangedService: SelectedModelChangedService) {
    /*
    Initialise subscriptions for retrieving selected dataset

    Parameters
    ----------
    uploadService : UploadService
      Service for uploading files
    selectedDatasetChangedService : SelectedDatasetChangedService
      Service for retrieving the selected dataset from a shared service
    selectedModelChangedService : SelectedModelChangedService
      Service for retrieving the selected model from a shared service
    */
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
    /*
    Unsubscribe from all subscriptions
    */
    this.selectedDatasetChanged.unsubscribe();
    this.selectedModelChanged.unsubscribe();
  }

  onFileSelected(event: any) {
    /*
    Save selected file if the type is correct

    Parameters
    ----------
    event : any
      Event of selected file
    */
    const file = event.target.files[0];
    if (!file || (this.uploadInformation.uploadFileTypes.length && !this.uploadInformation.uploadFileTypes.some(type => type === file.type)))
      return

    this.file = file
    this.fileName = file.name;
  }

  upload() {
    /*
    Upload file to backend and track progress
    */
    if (this.file && this.fileName) {
      this.errorMessage = "";
      this.successMessage = "";
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
    /*
    Update progress for current upload

    Parameters
    ----------
    loaded : number
      Number representing current transfer
    total : number
      Number representing total transfer
    */
    if (total)
      this.uploadProgress = Math.round(100 * (loaded / total));
    if (this.uploadProgress == 100)
      this.successMessage = "File successfully uploaded";
  }

  cancelUpload() {
    /*
    Cancel current upload
    */
    if (this.uploadSub)
      this.uploadSub.unsubscribe();
    this.reset();
  }

  reset() {
    /*
    Reset current upload and file
    */
    this.uploadProgress = null;
    this.uploadSub = null;
    this.file = null;
    this.fileName = '';
  }

  setDataset(value: string) {
    /*
    Set current dataset

    Parameters
    ----------
    value : string
      Name of current dataset
    */
    this.dataset = {name: value};
  }

  setModel(value: string) {
    /*
    Set current model

    Parameters
    ----------
    value : string
      Name of current model
    */
    this.model = {name: value, type: ''};
  }

  selectedModelTypeChanged(value: string) {
    /*
    Change selected model type (TF2, PyTorch, YOLOv3, YOLOv5)

    Parameters
    ----------
    value : string
      Name of selected model type
    */
    this.uploadInformation.apiEndpoint = value;
  }

  setErrorMessage(res: HttpErrorResponse) {
    /*
    Set error message and remove success message

    Parameters
    ----------
    res : HttpErrorResponse
      Error response containing upload errors
    */
    this.errorMessage = res.error;
    this.successMessage = "";
  }
}
