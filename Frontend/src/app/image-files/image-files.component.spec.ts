import {ComponentFixture, TestBed} from '@angular/core/testing';

import {ImageFilesComponent} from './image-files.component';
import {HttpClientModule} from "@angular/common/http";
import {SelectedImageChangedService} from "../shared-services/selected-image-changed-service";
import {ImageFile} from "./image-file";
import {of} from "rxjs";
import {ImageFilesService} from "./image-files.service";
import {BrowserModule, By} from "@angular/platform-browser";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";
import {DatasetListComponent} from "../dataset-list/dataset-list.component";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatSelectModule} from "@angular/material/select";
import {MatListModule} from "@angular/material/list";

describe('ImageFilesComponent', () => {
  let component: ImageFilesComponent;
  let fixture: ComponentFixture<ImageFilesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        BrowserAnimationsModule,
        MatFormFieldModule,
        MatSelectModule,
        MatListModule,
        BrowserModule
      ],
      providers: [
        SelectedImageChangedService
      ],
      declarations: [
        ImageFilesComponent,
        DatasetListComponent
      ]
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ImageFilesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#getImageFiles should create array of ImageFiles', () => {
    const imageFiles: ImageFile[] = [
      {name: "test_image1.jpg"},
      {name: "test_image2.jpg"},
      {name: "test_image3.jpg"},
    ]
    const imageFilesService = TestBed.inject(ImageFilesService);
    spyOn(imageFilesService, 'getImageFiles').and.returnValue(of(imageFiles));

    component.getImageFiles("test_dataset");

    expect(component.imageFiles).toBe(imageFiles);
  });

  it('#getImageFiles should create empty array of ImageFiles if no image files given', () => {
    const imageFiles: ImageFile[] = []
    const imageFilesService = TestBed.inject(ImageFilesService);
    spyOn(imageFilesService, 'getImageFiles').and.returnValue(of(imageFiles));

    component.getImageFiles("test_dataset");

    expect(component.imageFiles).toBe(imageFiles);
  });

  it('dataset subscription should trigger #getImageFiles', () => {
    const selectedDatasetChangedService = TestBed.inject(SelectedDatasetChangedService);
    const spy = spyOn(component, 'getImageFiles');

    selectedDatasetChangedService.publish("test_dataset")

    expect(spy).toHaveBeenCalledWith("test_dataset");
  });

  it('click should publish selected new file', () => {
    const selectedImageChangedService = TestBed.inject(SelectedImageChangedService);
    const event = {'option': {'value': "test_image1.jpg"}}
    spyOn(selectedImageChangedService, 'publish').withArgs("test_image1.jpg");

    component.onSelectedImageFileChanged(event)

    expect(selectedImageChangedService.publish).toHaveBeenCalledWith("test_image1.jpg")
  });

  it('should render several list elements if image files given', () => {
    const imageFiles: ImageFile[] = [
      {name: "test_image1.jpg"},
      {name: "test_image2.jpg"},
      {name: "test_image3.jpg"},
    ]
    const imageFilesService = TestBed.inject(ImageFilesService);
    spyOn(imageFilesService, 'getImageFiles').and.returnValue(of(imageFiles));

    component.getImageFiles("test_dataset");
    fixture.detectChanges();

    const queriedElements = fixture.debugElement.query(By.css('#image-files')).children;
    expect(queriedElements.length).toBe(3);
    expect(queriedElements[0].nativeElement.innerText).toEqual("test_image1.jpg")
    expect(queriedElements[1].nativeElement.innerText).toEqual("test_image2.jpg")
    expect(queriedElements[2].nativeElement.innerText).toEqual("test_image3.jpg")
  });

  it('should not render list elements if no image files given', () => {
    const noImageFiles: ImageFile[] = []
    const imageFilesService = TestBed.inject(ImageFilesService);
    spyOn(imageFilesService, 'getImageFiles').and.returnValue(of(noImageFiles));

    component.getImageFiles("test_dataset");
    fixture.detectChanges();

    const queriedElements = fixture.debugElement.query(By.css('#image-files')).children;
    expect(queriedElements.length).toBe(0);
  });

  it('onSelectedImageFileChanged')
});
