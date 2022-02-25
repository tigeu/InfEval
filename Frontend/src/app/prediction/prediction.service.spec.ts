import {TestBed} from '@angular/core/testing';

import {PredictionService} from './prediction.service';
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {Image} from "../image/image";
import {of} from "rxjs";
import {PredictionSettings} from "./prediction-settings";

describe('PredictionService', () => {
  let service: PredictionService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
      ],
    });
    service = TestBed.inject(PredictionService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('#getPrediction should return according image', () => {
    const http = TestBed.inject(HttpClient);
    const newImage: Image = {file: new File([""], "image.jpg")};
    const fakeImage: Image = {file: new File(["an"], "other_image.jpg")};
    const settings: PredictionSettings = {
      showPrediction: false,
      strokeSize: 10,
      showColored: true,
      showLabeled: true,
      fontSize: 35,
      classes: [],
      colors: [],
      minConf: 0,
      maxConf: 0,
      nmsIoU: 0,
      nmsScore: 0,
      onlyGroundTruth: false,
      groundTruthIoU: 0
    }

    spyOn(http, 'get').and.returnValue(of(newImage));

    service.getPrediction("dataset", "pred", "image.jpg", settings).subscribe(value => {
      expect(value).toBe(newImage);
      expect(value).not.toBe(fakeImage);
    });
  });
});
