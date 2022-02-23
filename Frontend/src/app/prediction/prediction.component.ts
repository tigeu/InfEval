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
  loading: boolean = false;
  showClasses: boolean[] = [];
  classColors: string[] = [];

  predictionSettings: PredictionSettings = {
    showPrediction: false,
    strokeSize: 10,
    showColored: true,
    showLabeled: true,
    fontSize: 35,
    classes: [],
    colors: [],
    minConf: 0,
    maxConf: 100,
    iou: 0,
    score: 0
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
      if (data.classes && data.colors) {
        this.showClasses = new Array(data.classes.length).fill(true);
        this.classColors = data.colors;
      }
      this.selectionChanged();
    })
    this.selectedImageChanged = this.selectedImageChangedService.newData.subscribe((data: any) => {
      this.selectedImage = data;
      this.selectionChanged();
    });
  }

  ngOnInit(): void {
  }

  ngOnDestroy(): void {
    this.selectedImageChanged.unsubscribe();
    this.selectedDatasetChanged.unsubscribe();
    this.selectedPredictionChanged.unsubscribe();
  }

  getPrediction() {
    this.loading = true;
    this.setClassColors();
    this.predictionService.getPrediction(this.selectedDataset.name, this.selectedPrediction.name, this.selectedImage, this.predictionSettings)
      .subscribe((prediction: Prediction) => {
        this.predictionChangedService.publish(prediction);
        this.loading = false;
      })
  }

  setClassColors() {
    if (this.selectedPrediction.classes) {
      let classes: string[] = [];
      let colors: string[] = [];
      for (let i = 0; i < this.selectedPrediction.classes?.length; i++) {
        if (this.showClasses[i]) {
          classes.push(this.selectedPrediction.classes[i]);
          colors.push(this.classColors[i]);
        }
      }
      this.predictionSettings.classes = classes;
      this.predictionSettings.colors = colors;
    }
  }

  selectionChanged() {
    this.validateNumbers();
    if (!this.predictionSettings.showPrediction)
      this.predictionChangedService.publish("");
    else if (this.selectedDataset && this.selectedPrediction && this.selectedImage) {
      this.getPrediction()
    }
  }

  validateNumbers() {
    this.validateConfidence();
    this.validateIoU();
    this.validateScore();
  }

  validateConfidence() {
    this.predictionSettings.minConf = Math.max(0, this.predictionSettings.minConf);
    this.predictionSettings.maxConf = Math.min(this.predictionSettings.maxConf, 100);
    if (this.predictionSettings.minConf > this.predictionSettings.maxConf)
      this.predictionSettings.minConf = this.predictionSettings.maxConf;
  }

  validateIoU() {
    if (this.predictionSettings.iou < 0)
      this.predictionSettings.iou = 0;
    else if (this.predictionSettings.iou > 1)
      this.predictionSettings.iou = 1;
  }

  validateScore() {
    if (this.predictionSettings.score < 0)
      this.predictionSettings.score = 0;
    else if (this.predictionSettings.score > 1)
      this.predictionSettings.score = 1;
  }

}
