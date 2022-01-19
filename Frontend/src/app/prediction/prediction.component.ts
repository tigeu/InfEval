import {Component, OnInit} from '@angular/core';
import {Subscription} from "rxjs";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";
import {SelectedImageChangedService} from "../shared-services/selected-image-changed-service";
import {PredictionSettings} from "./prediction-settings";
import {PredictionService} from "./prediction.service";
import {Prediction} from "./prediction";
import {PredictionChangedService} from "../shared-services/prediction-changed.service";
import {SelectedPredictionChangedService} from "../shared-services/selected-prediction-changed.service";
import {DatasetFile} from "../dataset-list/dataset-file";
import {PredictionFile} from "../prediction-list/prediction-file";

@Component({
  selector: 'app-prediction',
  templateUrl: './prediction.component.html',
  styleUrls: ['./prediction.component.css']
})
export class PredictionComponent implements OnInit {

  selectedDatasetChanged: Subscription;
  selectedDataset: DatasetFile = {name: ""};
  selectedPredictionChanged: Subscription;
  selectedPrediction: PredictionFile = {name: ""};
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
    this.selectedDatasetChanged = this.selectedDatasetChangedService.newData.subscribe((data: DatasetFile) => {
      this.selectedDataset = data;
      this.selectedPrediction = {name: ""};
      this.selectedImage = "";
      this.predictionSettings.showPrediction = false;
    });
    this.selectedPredictionChanged = this.selectedPredictionChangedService.newData.subscribe((data: any) => {
      this.selectedPrediction = data;
      this.selectionChanged();
    })
    this.selectedImageChanged = this.selectedImageChangedService.newData.subscribe((data: any) => {
      this.selectedImage = data;
      this.selectionChanged();
    });
  }

  ngOnInit(): void {

  }

  getPrediction() {
    this.predictionService.getPrediction(this.selectedDataset.name, this.selectedPrediction.name, this.selectedImage, this.predictionSettings)
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
