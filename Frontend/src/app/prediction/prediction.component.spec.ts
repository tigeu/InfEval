import {ComponentFixture, TestBed} from '@angular/core/testing';

import {PredictionComponent} from './prediction.component';
import {HttpClientModule} from "@angular/common/http";
import {of} from "rxjs";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";
import {SelectedImageChangedService} from "../shared-services/selected-image-changed-service";
import {Prediction} from "./prediction";
import {PredictionService} from "./prediction.service";
import {PredictionChangedService} from "../shared-services/prediction-changed.service";
import {SelectedPredictionChangedService} from "../shared-services/selected-prediction-changed.service";

describe('PredictionsComponent', () => {
  let component: PredictionComponent;
  let fixture: ComponentFixture<PredictionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
      ],
      declarations: [PredictionComponent]
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PredictionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#getPrediction should publish image', () => {
    const prediction: Prediction = {file: new File([""], "test_image.jpg")};
    const predictionService = TestBed.inject(PredictionService);
    const predictionChangedService = TestBed.inject(PredictionChangedService);
    spyOn(predictionService, 'getPrediction').and.returnValue(of(prediction));
    const spy = spyOn(predictionChangedService, 'publish');

    component.selectedDataset = {name: "test_dataset"};
    component.selectedImage = "test_image.jpg";

    component.getPrediction();

    expect(spy).toHaveBeenCalledWith(prediction)
  });

  it('dataset subscription should set selectedDataset and reset images and show selection', () => {
    const selectedDatasetChangedService = TestBed.inject(SelectedDatasetChangedService);
    const dataset = {name: "test_dataset"};

    selectedDatasetChangedService.publish(dataset)

    expect(component.selectedDataset).toEqual(dataset);
    expect(component.selectedPrediction).toEqual({name: ""});
    expect(component.selectedImage).toEqual("");
    expect(component.predictionSettings.showPrediction).toEqual(false);
  });

  it('prediction subscription should set selectedPrediction and trigger #selectionChanged', () => {
    const selectedPredictionChangedService = TestBed.inject(SelectedPredictionChangedService);
    const spy = spyOn(component, 'selectionChanged');
    const pred = {name: "test_pred"};

    selectedPredictionChangedService.publish(pred);

    expect(component.selectedPrediction).toEqual(pred);
    expect(spy).toHaveBeenCalled();
  });

  it('image subscription should set selectedImage and trigger selectionChanged', () => {
    const selectedImageChangedService = TestBed.inject(SelectedImageChangedService);
    const spy = spyOn(component, 'selectionChanged');

    selectedImageChangedService.publish("test_image.jpg")

    expect(component.selectedImage).toEqual("test_image.jpg");
    expect(spy).toHaveBeenCalled();
  });

  it('#selectionChanged should publish empty string if show gt not checked anymore', () => {
    const predictionChangedService = TestBed.inject(PredictionChangedService);
    const spy = spyOn(predictionChangedService, 'publish');

    component.selectionChanged();

    expect(spy).toHaveBeenCalledWith("");
  });

  it('#selectionChanged should trigger #getGroundTruth if dataset, pred and image are selected', () => {
    const spy = spyOn(component, 'getPrediction');
    component.predictionSettings.showPrediction = true;
    component.selectedDataset = {name: "test_dataset"}
    component.selectedPrediction = {name: "test_pred"};
    component.selectedImage = "test_image.jpg";

    component.selectionChanged();

    expect(spy).toHaveBeenCalled();
  });

  it('#selectionChanged should not trigger #getPrediction if dataset, pred and image are not selected', () => {
    const spy = spyOn(component, 'getPrediction');
    component.selectedDataset = {name: ""};
    component.selectedPrediction = {name: ""};
    component.selectedImage = "";

    component.selectionChanged();

    expect(spy).not.toHaveBeenCalled();
  });
});
