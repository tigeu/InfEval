import {TestBed} from '@angular/core/testing';

import {PredictionListService} from './prediction-list.service';
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {PredictionFile} from "./prediction-file";
import {of} from "rxjs";

describe('PredictionListService', () => {
  let service: PredictionListService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
      ],
    });
    service = TestBed.inject(PredictionListService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('#getPredictionList should return array of PredictionFiles', () => {
    const http = TestBed.inject(HttpClient);
    const predictionFiles: PredictionFile[] = [
      {name: "pred1"},
      {name: "pred2"},
      {name: "pred3"},
    ]

    const fakePrediction: PredictionFile = {name: "other_pred"};
    spyOn(http, 'get').and.returnValue(of(predictionFiles));

    service.getPredictionList("dataset").subscribe(value => {
      expect(value).toBe(predictionFiles);
      expect(value).not.toContain(fakePrediction);
    });
  });

  it('#getPredictionList should return empty array if no predictions', () => {
    const http = TestBed.inject(HttpClient);
    const predictionsFiles: PredictionFile[] = []

    spyOn(http, 'get').and.returnValue(of(predictionsFiles));

    service.getPredictionList("dataset").subscribe(value => {
      expect(value).toBe(predictionsFiles);
    });
  });

  it('#getPredictionList should return array with one element if only one prediction', () => {
    const http = TestBed.inject(HttpClient);
    const predictionFiles: PredictionFile[] = [
      {name: "pred1"}
    ]

    spyOn(http, 'get').and.returnValue(of(predictionFiles));

    service.getPredictionList("dataset").subscribe(value => {
      expect(value).toBe(predictionFiles);
    });
  });
});
