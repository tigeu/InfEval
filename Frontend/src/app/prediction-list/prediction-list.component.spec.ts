import {ComponentFixture, TestBed} from '@angular/core/testing';

import {PredictionListComponent} from './prediction-list.component';
import {HttpClientModule} from "@angular/common/http";
import {of} from "rxjs";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";
import {PredictionFile} from "./prediction-file";
import {PredictionListService} from "./prediction-list.service";
import {SelectedPredictionChangedService} from "../shared-services/selected-prediction-changed.service";

describe('PredictionListComponent', () => {
  let component: PredictionListComponent;
  let fixture: ComponentFixture<PredictionListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
      ],
      declarations: [PredictionListComponent]
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PredictionListComponent);
    component = fixture.componentInstance;
    component.selectedDataset = {name: "test_dataset"};
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('dataset subscription should update selectedDataset', () => {
    const selectedDatasetChangedService = TestBed.inject(SelectedDatasetChangedService);
    const dataset = {name: "test_dataset"}

    selectedDatasetChangedService.publish(dataset);

    expect(component.selectedDataset).toEqual(dataset);
  });

  it('#getPredictionList should set predictionList', () => {
    const predictionFiles: PredictionFile[] = [
      {name: "pred1"},
      {name: "pred2"},
      {name: "pred3"},
    ]

    const predictionListService = TestBed.inject(PredictionListService);
    spyOn(predictionListService, 'getPredictionList').and.returnValue(of(predictionFiles));

    component.getPredictionList("dataset");

    expect(component.predictionList).toBe(predictionFiles);
  });

  it('#getPredictionList should create set predictionList to empty array if no prediction exist', () => {
    const predictionFiles: PredictionFile[] = []
    const predictionListService = TestBed.inject(PredictionListService);
    spyOn(predictionListService, 'getPredictionList').and.returnValue(of(predictionFiles));

    component.getPredictionList("dataset");

    expect(component.predictionList).toBe(predictionFiles);
  });

  it('click should publish new selected prediction', () => {
    const selectedPredictionChangedService = TestBed.inject(SelectedPredictionChangedService);
    spyOn(selectedPredictionChangedService, 'publish').withArgs("pred");

    component.selectedPredictionChanged("pred");

    expect(selectedPredictionChangedService.publish).toHaveBeenCalledWith("pred")
  });
});
