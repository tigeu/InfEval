import {ComponentFixture, discardPeriodicTasks, fakeAsync, TestBed, tick} from '@angular/core/testing';

import {UploadMainComponent} from './upload-main.component';
import {HttpClientModule} from "@angular/common/http";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatSelectModule} from "@angular/material/select";
import {MatTabsModule} from "@angular/material/tabs";
import {UploadComponent} from "../upload/upload.component";
import {MatIconModule} from "@angular/material/icon";

describe('UploadMainComponent', () => {
  let component: UploadMainComponent;
  let fixture: ComponentFixture<UploadMainComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        FormsModule,
        ReactiveFormsModule,
        BrowserAnimationsModule,
        MatFormFieldModule,
        MatSelectModule,
        MatTabsModule,
        MatIconModule
      ],
      declarations: [
        UploadMainComponent,
        UploadComponent
      ]
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UploadMainComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#setDatasetName should call next on subject', () => {
    const spy = spyOn(component.datasetNameSubject, "next")

    component.setDatasetName("test_dataset1");

    expect(spy).toHaveBeenCalledWith("test_dataset1")
  });

  it('#setDatasetName should set datasetname after debouncetime', fakeAsync(() => {
    component.setDatasetName("test_dataset1");

    tick(300);

    expect(component.datasetName).toEqual("test_dataset1");
    discardPeriodicTasks();
  }));
});
