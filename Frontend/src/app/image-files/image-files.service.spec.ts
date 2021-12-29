import {TestBed} from '@angular/core/testing';

import {ImageFilesService} from './image-files.service';
import {HttpClient} from "@angular/common/http";
import {ImageFile} from "./image-file";
import {HttpClientTestingModule} from "@angular/common/http/testing";
import {of} from "rxjs";

describe('ImageFilesService', () => {
  let service: ImageFilesService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
      ],
      providers: []
    });
    service = TestBed.inject(ImageFilesService);
  });

  it('should be created', () => {
    service = TestBed.inject(ImageFilesService);

    expect(service).toBeTruthy();
  });

  it('#getImageFiles should return array of Imagefiles', () => {
    const http = TestBed.inject(HttpClient);
    const imageFiles: ImageFile[] = [
      {name: "test_image1.jpg"},
      {name: "test_image2.jpg"},
      {name: "test_image3.jpg"},
    ]

    const fakeImageFile: ImageFile = {name: "other_image.jpg"};
    spyOn(http, 'get').and.returnValue(of(imageFiles));

    service.getImageFiles("test_dataset").subscribe(value => {
      expect(value).toBe(imageFiles);
      expect(value).not.toContain(fakeImageFile);
    });
  });

  it('#getImageFiles should return empty array if no image files', () => {
    const http = TestBed.inject(HttpClient);
    const imageFiles: ImageFile[] = []

    spyOn(http, 'get').and.returnValue(of(imageFiles));

    service.getImageFiles("test_dataset").subscribe(value => {
      expect(value).toBe(imageFiles);
    });
  });

  it('#getImageFiles should return array with one element if only one image files', () => {
    const http = TestBed.inject(HttpClient);
    const imageFiles: ImageFile[] = [
      {name: "test_image1.jpg"}
    ]

    spyOn(http, 'get').and.returnValue(of(imageFiles));

    service.getImageFiles("test_dataset").subscribe(value => {
      expect(value).toBe(imageFiles);
    });
  });
})
