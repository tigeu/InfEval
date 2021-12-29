import {TestBed} from '@angular/core/testing';

import {ImageService} from './image.service';
import {HttpClient} from "@angular/common/http";
import {Image} from "./image";
import {HttpClientTestingModule} from "@angular/common/http/testing";
import {of} from "rxjs";

describe('ImageService', () => {
  let service: ImageService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
      ],
      providers: []
    });
    service = TestBed.inject(ImageService);
  });

  it('should be created', () => {
    service = TestBed.inject(ImageService);

    expect(service).toBeTruthy();
  });

  it('#getImage should return according image', () => {
    const http = TestBed.inject(HttpClient);
    const newImage: Image = {file: new File([""], "test_image.jpg")};
    const fakeImage: Image = {file: new File(["an"], "other_image.jpg")};

    spyOn(http, 'get').and.returnValue(of(newImage));

    service.getImage("test_data_set", "test_image.jpg").subscribe(value => {
      expect(value).toBe(newImage);
      expect(value).not.toBe(fakeImage);
    });
  });
})
