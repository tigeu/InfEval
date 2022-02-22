import {ComponentFixture, TestBed} from '@angular/core/testing';

import {OverviewComponent} from './overview.component';
import {HttpClientModule} from "@angular/common/http";
import {OverviewService} from "./overview.service";
import {OverviewDatasetFile} from "./overview-dataset-file";
import {OverviewPredictionFile} from "./overview-prediction-file";
import {OverviewModelFile} from "./overview-model-file";
import {OverviewTaskFile} from "./overview-task-file";
import {of} from "rxjs";

describe('OverviewComponent', () => {
  let component: OverviewComponent;
  let fixture: ComponentFixture<OverviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
      ],
      declarations: [OverviewComponent]
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(OverviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#getOverviewData should set lists', () => {
    const service = TestBed.inject(OverviewService);
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

    spyOn(service, "getOverviewData").and.returnValue(of(response));

    component.getOverviewData();

    expect(component.datasetList).toEqual(datasets);
    expect(component.predictionList).toEqual(predictions);
    expect(component.modelList).toEqual(models);
    expect(component.tasksList).toEqual(tasks);
  });

  it('#deleteDataset should call getOverviewData', () => {
    const service = TestBed.inject(OverviewService);
    const spy = spyOn(component, "getOverviewData");
    spyOn(service, "deleteDataset").and.returnValue(of({}));

    component.deleteDataset("dataset");
    expect(spy).toHaveBeenCalled();
  });

  it('#deletePrediction should call getOverviewData', () => {
    const service = TestBed.inject(OverviewService);
    const spy = spyOn(component, "getOverviewData");
    spyOn(service, "deletePrediction").and.returnValue(of({}));

    component.deletePrediction("prediction");
    expect(spy).toHaveBeenCalled();
  });

  it('#deleteModel should call getOverviewData', () => {
    const service = TestBed.inject(OverviewService);
    const spy = spyOn(component, "getOverviewData");
    spyOn(service, "deleteModel").and.returnValue(of({}));

    component.deleteModel("model");
    expect(spy).toHaveBeenCalled();
  });

  it('#deleteTask should call getOverviewData', () => {
    const service = TestBed.inject(OverviewService);
    const spy = spyOn(component, "getOverviewData");
    spyOn(service, "deleteTask").and.returnValue(of({}));

    component.deleteTask("task");
    expect(spy).toHaveBeenCalled();
  });
});
