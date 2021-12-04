import {ComponentFixture, TestBed} from '@angular/core/testing';

import {ImageFilesComponent} from './image-files.component';
import {HttpClientModule} from "@angular/common/http";
import {SelectedImageChangedService} from "../shared-services/selected-image-changed-service";
import {ImageFile} from "./image-file";
import {of} from "rxjs";
import {ImageFilesService} from "./image-files.service";
import {By} from "@angular/platform-browser";

describe('ImageFilesComponent', () => {
  let component: ImageFilesComponent;
  let fixture: ComponentFixture<ImageFilesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientModule
      ],
      providers: [
        SelectedImageChangedService
      ],
      declarations: [ImageFilesComponent]
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

    component.getImageFiles();

    expect(component.imageFiles).toBe(imageFiles);
  });

  it('#getImageFiles should create empty array of ImageFiles if no image files given', () => {
    const imageFiles: ImageFile[] = []
    const imageFilesService = TestBed.inject(ImageFilesService);
    spyOn(imageFilesService, 'getImageFiles').and.returnValue(of(imageFiles));

    component.getImageFiles();

    expect(component.imageFiles).toBe(imageFiles);
  });

  it('click should publish selected new file', () => {
    const selectedImageChangedService = TestBed.inject(SelectedImageChangedService);
    const ul = fixture.debugElement.query(By.css('#image-files'));
    const htmlElement = document.createElement('li')
    htmlElement.innerText = "test_image1.jpg"
    spyOn(selectedImageChangedService, 'publish').withArgs("test_image1.jpg");

    ul.triggerEventHandler('click', {target: htmlElement});

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

    component.getImageFiles();
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

    component.getImageFiles();
    fixture.detectChanges();

    const queriedElements = fixture.debugElement.query(By.css('#image-files')).children;
    expect(queriedElements.length).toBe(0);
  });
});
