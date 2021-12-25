import {TestBed} from '@angular/core/testing';

import {UploadService} from './upload.service';
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {UploadTypes} from "./UploadTypes";

describe('UploadService', () => {
  let service: UploadService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
      ],
    });
    service = TestBed.inject(UploadService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('#upload should call put', () => {
    const http = TestBed.inject(HttpClient);
    const file = new File(["content"], "test.txt");

    spyOn(http, "put")

    service.upload("test.txt", file, UploadTypes.Dataset);

    expect(http.put).toHaveBeenCalled();
  });
});
