import {Component, OnInit} from '@angular/core';
import {Subscription} from "rxjs";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";
import {SelectedImageChangedService} from "../shared-services/selected-image-changed-service";
import {PredictionSettings} from "./prediction-settings";
import {PredictionService} from "./prediction.service";
import {Prediction} from "./prediction";
import {PredictionChangedService} from "../shared-services/prediction-changed.service";
import {SelectedPredictionChangedService} from "../shared-services/selected-prediction-changed.service";

@Component({
  selector: 'app-prediction',
  templateUrl: './predictions.component.html',
  styleUrls: ['./predictions.component.css']
})
export class PredictionsComponent implements OnInit {

  selectedDatasetChanged: Subscription;
  selectedDataset: string = "";
  selectedPredictionChanged: Subscription;
  selectedPrediction: string = "";
  selectedImageChanged: Subscription;
  selectedImage: string = "";

  predictionSettings: PredictionSettings = {
    showPrediction: false,
    strokeSize: 10,
    showColored: true,
    showLabeled: true,
    fontSize: 35
  }

  constructor(private predictionService: PredictionService,
              private selectedDatasetChangedService: SelectedDatasetChangedService,
              private selectedPredictionChangedService: SelectedPredictionChangedService,
              private selectedImageChangedService: SelectedImageChangedService,
              private predictionChangedService: PredictionChangedService) {
    this.selectedDatasetChanged = this.selectedDatasetChangedService.newData.subscribe((data: string) => {
      this.selectedDataset = data;
      this.selectedPrediction = "";
      this.selectedImage = "";
      this.predictionSettings.showPrediction = false;
    });
    this.selectedPredictionChanged = this.selectedPredictionChangedService.newData.subscribe((data: any) => {
      this.selectedPrediction = data;
    })
    this.selectedImageChanged = this.selectedImageChangedService.newData.subscribe((data: any) => {
      this.selectedImage = data;
      this.selectionChanged();
    });
  }

  ngOnInit(): void {

  }

  getPrediction() {
    this.predictionService.getPrediction(this.selectedDataset, this.selectedPrediction, this.selectedImage, this.predictionSettings)
      .subscribe((prediction: Prediction) => {
        this.predictionChangedService.publish(prediction);
      })
  }

  selectionChanged() {
    if (!this.predictionSettings.showPrediction)
      this.predictionChangedService.publish("");
    else if (this.selectedDataset && this.selectedPrediction && this.selectedImage) {
      this.getPrediction()
    }
  }

}
