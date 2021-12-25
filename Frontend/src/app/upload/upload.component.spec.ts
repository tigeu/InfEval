import {ComponentFixture, TestBed} from '@angular/core/testing';

import {UploadComponent} from './upload.component';
import {HttpClientModule, HttpEventType, HttpProgressEvent} from "@angular/common/http";
import {MatIconModule} from "@angular/material/icon";
import {UploadService} from "./upload.service";
import {of, Subscription} from "rxjs";
import {UploadFileTypes} from "./UploadFileTypes";
import {UploadTypes} from "./UploadTypes";

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
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#onFileSelected should update progress and finally reset', () => {
    const uploadService = TestBed.inject(UploadService);
    const file = new File(["content"], "test.txt", {type: UploadFileTypes.Compressed});
    const event = {target: {files: [file]}}

    const httpEvent = of({type: HttpEventType.UploadProgress, loaded: 7, total: 10} as HttpProgressEvent)
    spyOn(uploadService, "upload").withArgs("test.txt", file, "test", UploadTypes.Dataset)
      .and.returnValue(httpEvent);
    spyOn(component, "reset");
    spyOn(component, "updateProgress").withArgs(7, 10);

    component.onFileSelected(event)

    expect(uploadService.upload).toHaveBeenCalled();
    expect(component.reset).toHaveBeenCalled();
    expect(component.updateProgress).toHaveBeenCalled();
  });

  it('#onFileSelected should return if file is not given', () => {
    const uploadService = TestBed.inject(UploadService);
    const event = {target: {files: []}}

    spyOn(uploadService, "upload");
    spyOn(component, "reset");
    spyOn(component, "updateProgress");

    component.onFileSelected(event);

    expect(uploadService.upload).not.toHaveBeenCalled();
    expect(component.reset).not.toHaveBeenCalled();
    expect(component.updateProgress).not.toHaveBeenCalled();
  })

  it('#onFileSelected should return if file type is not compressed', () => {
    const uploadService = TestBed.inject(UploadService);
    const file = new File(["content"], "test.txt");
    const event = {target: {files: [file]}}

    spyOn(uploadService, "upload");
    spyOn(component, "reset");
    spyOn(component, "updateProgress");

    component.onFileSelected(event);

    expect(uploadService.upload).not.toHaveBeenCalled();
    expect(component.reset).not.toHaveBeenCalled();
    expect(component.updateProgress).not.toHaveBeenCalled();
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
    expect(component.fileName).not.toBeTruthy();
  })
});
