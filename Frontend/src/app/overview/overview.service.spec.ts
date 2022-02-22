import {TestBed} from '@angular/core/testing';

import {OverviewService} from './overview.service';
import {HttpClient, HttpClientModule, HttpResponse} from "@angular/common/http";
import {of} from "rxjs";
import {OverviewDatasetFile} from "./overview-dataset-file";
import {OverviewPredictionFile} from "./overview-prediction-file";
import {OverviewModelFile} from "./overview-model-file";
import {OverviewTaskFile} from "./overview-task-file";

describe('OverviewService', () => {
  let service: OverviewService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
      ],
    });
    service = TestBed.inject(OverviewService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('#getOverviewData should return OverviewFile', () => {
    const http = TestBed.inject(HttpClient);
    const datasets: OverviewDatasetFile[] = [
      {"name": "data1", "groundTruth": true, "predictions": false, "uploaded": new Date()}];
    const predictions: OverviewPredictionFile[] = [
      {"name": "pred1", "dataset": "data1", "uploaded": new Date()}
    ];
    const models: OverviewModelFile[] = [
      {"name": "model1", "type": "tf2", "labelMap": true, "uploaded": new Date()}
    ];
    const tasks: OverviewTaskFile[] = [
      {
        "name": "task1", "description": "desc", "progress": 50, "fileName": "file",
        "started": new Date(), "finished": new Date(), "dataset": "data1", "model": "model1"
      }
    ];

    const response = {"datasets": datasets, "predictions": predictions, "models": models, "tasks": tasks}

    spyOn(http, 'get').and.returnValue(of(response));

    service.getOverviewData()
      .subscribe(res => {
        expect(res).toBe(response);
      });
  });

  it('#deleteDataset should return httpResponse', () => {
    const http = TestBed.inject(HttpClient);
    const response = new HttpResponse({status: 200})

    spyOn(http, 'delete').and.returnValue(of(response));

    service.deleteDataset("dataset")
      .subscribe(res => {
        expect(res).toBe(response);
      });
  });

  it('#deletePrediction should return httpResponse', () => {
    const http = TestBed.inject(HttpClient);
    const response = new HttpResponse({status: 200})

    spyOn(http, 'delete').and.returnValue(of(response));

    service.deletePrediction("prediction")
      .subscribe(res => {
        expect(res).toBe(response);
      });
  });

  it('#deleteModel should return httpResponse', () => {
    const http = TestBed.inject(HttpClient);
    const response = new HttpResponse({status: 200})

    spyOn(http, 'delete').and.returnValue(of(response));

    service.deleteModel("model")
      .subscribe(res => {
        expect(res).toBe(response);
      });
  });

  it('#deleteTask should return httpResponse', () => {
    const http = TestBed.inject(HttpClient);
    const response = new HttpResponse({status: 200})

    spyOn(http, 'delete').and.returnValue(of(response));

    service.deleteTask("task")
      .subscribe(res => {
        expect(res).toBe(response);
      });
  });
});
