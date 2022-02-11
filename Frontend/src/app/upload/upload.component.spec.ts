import {ComponentFixture, TestBed} from '@angular/core/testing';

import {UploadComponent} from './upload.component';
import {HttpClientModule, HttpEventType, HttpProgressEvent} from "@angular/common/http";
import {MatIconModule} from "@angular/material/icon";
import {UploadService} from "./upload.service";
import {of, Subscription} from "rxjs";
import {UploadFileTypes} from "./UploadFileTypes";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";
import {SelectedModelChangedService} from "../shared-services/selected-model-changed.service";

describe('UploadComponent', () => {
  let component: UploadComponent;
  let fixture: ComponentFixture<UploadComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [UploadComponent],
      imports: [
        HttpClientModule,
        MatIconModule,
      ],
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UploadComponent);
    component = fixture.componentInstance;

    const uploadInformation = {
      isDataset: false,
      isModel: false,
      uploadFileTypes: [UploadFileTypes.Zip],
      uploadFileEnding: ".zip",
      apiEndpoint: "dataset"
    };
    component.dataset = {name: "test_dataset"};
    component.uploadInformation = uploadInformation;

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('dataset subscription should set datasetName', () => {
    const selectedDatasetChangedService = TestBed.inject(SelectedDatasetChangedService);
    const dataset = {name: 'test_dataset'}

    selectedDatasetChangedService.publish(dataset)

    expect(component.dataset).toEqual(dataset);
  });

  it('model subscription should set datasetName', () => {
    const selectedModelChangedService = TestBed.inject(SelectedModelChangedService);
    const model = {name: 'test_model', type: ''}

    selectedModelChangedService.publish(model)

    expect(component.model).toEqual(model);
  });

  it('#upload should update progress and finally reset', () => {
    const uploadService = TestBed.inject(UploadService);
    const file = new File(["content"], "test.txt", {type: UploadFileTypes.Zip});

    const httpEvent = of({type: HttpEventType.UploadProgress, loaded: 7, total: 10} as HttpProgressEvent)
    component.file = file
    component.fileName = "test.txt"

    spyOn(uploadService, "upload")
      .withArgs("test.txt", file, "test_dataset", "", "dataset")
      .and.returnValue(httpEvent);
    spyOn(component, "reset");
    spyOn(component, "updateProgress").withArgs(7, 10);

    component.upload()

    expect(uploadService.upload).toHaveBeenCalled();
    expect(component.reset).toHaveBeenCalled();
    expect(component.updateProgress).toHaveBeenCalled();
  });

  it('#upload not do anything when file is not set', () => {
    const uploadService = TestBed.inject(UploadService);
    spyOn(uploadService, "upload");

    component.upload()

    expect(uploadService.upload).not.toHaveBeenCalled();
  });

  it('#onFileSelected should set file and fileName', () => {
    const file = new File(["content"], "test.txt", {type: UploadFileTypes.Zip});
    const event = {target: {files: [file]}}

    component.onFileSelected(event);

    expect(component.file).toBe(file);
    expect(component.fileName).toEqual("test.txt")
  })


  it('#onFileSelected should return if file is not given', () => {
    const event = {target: {files: []}}

    component.onFileSelected(event);

    expect(component.file).not.toBeTruthy()
    expect(component.fileName).not.toBeTruthy()
  })

  it('#onFileSelected should return if file type is not compressed', () => {
    const file = new File(["content"], "test.txt");
    const event = {target: {files: [file]}}

    component.onFileSelected(event);

    expect(component.file).not.toBeTruthy()
    expect(component.fileName).not.toBeTruthy()
  })

  it('#updateProgress should update the value correctly', () => {
    component.updateProgress(7, 10);

    expect(component.uploadProgress).toBe(70)
  });

  it('#updateProgress should not update the value if total is 0', () => {
    component.updateProgress(0, 0);

    expect(component.uploadProgress).not.toBeTruthy();
  });

  it('#cancelUpload should unsubscribe and call reset', () => {
    component.uploadSub = new Subscription();
    spyOn(component, "reset");

    component.cancelUpload();

    expect(component.uploadSub.closed).toBeTruthy();
    expect(component.reset).toHaveBeenCalled();
  });

  it('#reset should uploadProgress and uploadSub to null and fileName to ""', () => {
    component.uploadProgress = 10;
    component.uploadSub = new Subscription();

    component.reset();

    expect(component.uploadProgress).not.toBeTruthy();
    expect(component.uploadSub).not.toBeTruthy();
    expect(component.file).not.toBeTruthy();
    expect(component.fileName).not.toBeTruthy();
  })

  it('#ngOnDestroy unsubscribes from all subscriptions', () => {
    const selectedDatasetChangedSpy = spyOn(component.selectedDatasetChanged, 'unsubscribe');

    component.ngOnDestroy();

    expect(selectedDatasetChangedSpy).toHaveBeenCalled();
  });

  it('#setDataset should set dataset', () => {
    component.setDataset("test_dataset");

    expect(component.dataset.name).toEqual("test_dataset");
  });

  it('#setModel should set model', () => {
    component.setModel("test_model");

    expect(component.model.name).toEqual("test_model");
  });

  it('#selectedModelTypeChanged should set apiEndpoint', () => {
    component.selectedModelTypeChanged("new_endpoint");

    expect(component.uploadInformation.apiEndpoint).toEqual("new_endpoint");
  });
});
