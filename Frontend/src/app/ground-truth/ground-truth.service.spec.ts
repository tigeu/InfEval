import {TestBed} from '@angular/core/testing';

import {GroundTruthService} from './ground-truth.service';
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {Image} from "../image/image";
import {of} from "rxjs";
import {GroundTruthSettings} from "./ground-truth-settings";

describe('GroundTruthService', () => {
  let service: GroundTruthService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
      ]
    });
    service = TestBed.inject(GroundTruthService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('#getGroundTruth should return according image', () => {
    const http = TestBed.inject(HttpClient);
    const newImage: Image = {file: new File([""], "test_image.jpg")};
    const fakeImage: Image = {file: new File(["an"], "other_image.jpg")};
    const settings: GroundTruthSettings = {
      showGroundTruth: false,
      strokeSize: 10,
      showColored: true,
      showLabeled: true,
      fontSize: 35
    }

    spyOn(http, 'get').and.returnValue(of(newImage));

    service.getGroundTruth("test_data_set", "test_image.jpg", settings).subscribe(value => {
      expect(value).toBe(newImage);
      expect(value).not.toBe(fakeImage);
    });
  });
});
