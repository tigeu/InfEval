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
import {PascalMetricFile} from "./pascal-metric-file";
import {CocoMetricFile} from "./coco-metric-file";

@Component({
  selector: 'app-prediction',
  templateUrl: './prediction.component.html',
  styleUrls: ['./prediction.component.css']
})
export class PredictionComponent implements OnInit {
  /*
  Component that gets provides options for showing and filtering predictions values for currently selected dataset. Also
  allow to calculate coco and pascal voc metric with current settings.

  Attributes
  ----------
  predictionService : PredictionService
    Service for retrieving an image with drawn prediction values
  selectedDatasetChangedService : SelectedDatasetChangedService
    Service for retrieving the selected dataset from a shared service
  selectedPredictionChangedService : SelectedPredictionChangedService
    Service for retrieving the selected predictions from a shared service
  selectedImageChangedService : SelectedImageChangedService
    Service for retrieving the selected image
  predictionChangedService : PredictionChangedService
    Service for publishing the retrieved image with drawn prediction values
  selectedDatasetChanged : Subscription
    Subscription to retrieve currently selected dataset
  selectedDataset : DatasetFile
    Currently selected dataset
  selectedPredictionChanged : Subscription
    Subscription to retrieve currently selected prediction file
  selectedPrediction : PredictionFile
    Currently selected prediction file
  selectedImageChanged : Subscription
    Subscription to retrieve currently selected image name
  selectedImage : string
    Name of currently selected image
  loading : boolean
    Variable indicating whether the request has been finished yet
  showClasses : boolean[]
    Boolean array, each entry representing a class from the current dataset, indicating whether the class should be
    considered
  classColors : string[]
    String array, each entry representing a class from the current dataset, containing the selected colors
  predictionSettings : PredictionSettings
    Class for saving several different settings that are used to customize the drawings
  calculatingMetric : boolean
    Indicates whether metric is currently being calculated
  showErrorMessage : boolean
    Indicates whether error message for metric should be shown
  pascalMetric : PascalMetricFile
    File to store pascal voc results
  cocoMetric : CocoMetric
    File to store coco results
  metricHeader : String
    Header to be displayed after calculating (showing whether it was for image or dataset)

  Methods
  -------
  getPrediction()
    Calls service to retrieve the prediction drawings and publish the image
  calculateMetric(forDataset : boolean = false)
    Call currently selected metric to be calculated with an indicator whether it should be calculated for whole dataset
  setMetricHeader(forDataset : boolean = false)
    Set metric header (showing whether it was for image or dataset)
  calculatePascalMetric(forDataset : boolean = false)
    Calculate pascal metric based on current settings
  calculateCocoMetric(forDataset : boolean = false)
    Calculate coco metric based on current settings
  resetMetric()
    Reset last metric results
  setClassColors(prediction: string)
    Initialise showClasses and classColors values from currently selected dataset
  selectionChanged()
    Any setting was changed by user and a new image has to be requested
  validateNumbers()
    Call validation methods for confidence interval and NMS
  validateConfidence()
    Validate confidence interval so that min and max are valid ([0,100]) and min<max
  validateIoU()
    Validate IoU value so that it is valid ([0,1])
  validateScore()
    Validate score value so that it is valid ([0,1])
  validateGroundTruthIoU()
    Validate ground truth IoU value (used for overlapping) so that it is valid ([0,1])
  */
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
    nmsIoU: 0,
    nmsScore: 0,
    onlyGroundTruth: false,
    groundTruthIoU: 0,
    groundTruthTransparent: false,
    metric: "",
    IoU: 0
  }

  calculatingMetric: boolean = false;
  showErrorMessage: boolean = false;
  pascalMetric?: PascalMetricFile;
  cocoMetric?: CocoMetricFile;
  metricHeader: string = "";

  constructor(private predictionService: PredictionService,
              private selectedDatasetChangedService: SelectedDatasetChangedService,
              private selectedPredictionChangedService: SelectedPredictionChangedService,
              private selectedImageChangedService: SelectedImageChangedService,
              private predictionChangedService: PredictionChangedService) {
    /*
    Initialise subscriptions for retrieving selected dataset, selected prediction and selected image

    Parameters
    ----------
    predictionService : PredictionService
      Service for retrieving an image with drawn prediction values
    selectedDatasetChangedService : SelectedDatasetChangedService
      Service for retrieving the selected dataset from a shared service
    selectedPredictionChangedService : SelectedPredictionChangedService
      Service for retrieving the selected predictions from a shared service
    selectedImageChangedService : SelectedImageChangedService
      Service for retrieving the selected image
    predictionChangedService : PredictionChangedService
      Service for publishing the retrieved image with drawn prediction values
    */
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
    /*
    Unsubscribe from all subscriptions
    */
    this.selectedImageChanged.unsubscribe();
    this.selectedDatasetChanged.unsubscribe();
    this.selectedPredictionChanged.unsubscribe();
  }

  getPrediction() {
    /*
    Calls service to retrieve the prediction drawings and publish the image
    */
    this.loading = true;
    this.setClassColors();
    this.predictionService.getPrediction(this.selectedDataset.name, this.selectedPrediction.name, this.selectedImage, this.predictionSettings)
      .subscribe((prediction: Prediction) => {
        this.predictionChangedService.publish(prediction);
        this.loading = false;
      })
  }

  calculateMetric(forDataset: boolean = false) {
    /*
    Call currently selected metric to be calculated with an indicator whether it should be calculated for whole dataset

    Parameters
    ----------
    forDataset : boolean
      Indicating whether metric should be calculated for whole dataset or for image
    */
    this.showErrorMessage = false;
    this.setMetricHeader(forDataset);
    if (this.predictionSettings.metric == "coco")
      this.calculateCocoMetric(forDataset);
    else if (this.predictionSettings.metric == "pascal")
      this.calculatePascalMetric(forDataset);
  }

  setMetricHeader(forDataset: boolean = false) {
    /*
    Set metric header (showing whether it was for image or dataset)

    Parameters
    ----------
    forDataset : boolean
      Indicating whether metric should be calculated for whole dataset or for image
    */
    if (forDataset)
      this.metricHeader = `Results for ${this.selectedDataset.name}`;
    else
      this.metricHeader = `Results for ${this.selectedImage}`;
  }

  calculatePascalMetric(forDataset: boolean = false) {
    /*
    Calculate pascal metric based on current settings

    Parameters
    ----------
    forDataset : boolean
      Indicating whether metric should be calculated for whole dataset or for image
    */
    this.resetMetric();
    this.calculatingMetric = true;
    let fileName = this.selectedImage;
    if (forDataset)
      fileName = "";
    this.predictionService.getPascalMetric(this.selectedDataset.name, this.selectedPrediction.name, fileName, this.predictionSettings)
      .subscribe({
        next: (pascalMetricFile: PascalMetricFile) => {
          this.pascalMetric = pascalMetricFile;
          this.calculatingMetric = false;
        },
        error: () => {
          this.calculatingMetric = false;
          this.showErrorMessage = true;
        }
      });
  }

  calculateCocoMetric(forDataset: boolean = false) {
    /*
    Calculate coco metric based on current settings

    Parameters
    ----------
    forDataset : boolean
      Indicating whether metric should be calculated for whole dataset or for image
    */
    this.resetMetric();
    this.calculatingMetric = true;
    let fileName = this.selectedImage;
    if (forDataset)
      fileName = "";
    this.predictionService.getCocoMetric(this.selectedDataset.name, this.selectedPrediction.name, fileName, this.predictionSettings)
      .subscribe({
        next: (cocoMetricFile: CocoMetricFile) => {
          this.cocoMetric = cocoMetricFile;
          this.calculatingMetric = false;
        },
        error: () => {
          this.calculatingMetric = false;
          this.showErrorMessage = true;
        }
      });
  }

  resetMetric() {
    /*
    Reset last metric results
    */
    this.pascalMetric = undefined;
    this.cocoMetric = undefined;
  }

  setClassColors() {
    /*
    Initialise showClasses and classColors values from currently selected dataset
    */
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
    /*
    Any setting was changed by user and a new image has to be requested
    */
    this.validateNumbers();
    if (!this.predictionSettings.showPrediction)
      this.predictionChangedService.publish("");
    else if (this.selectedDataset && this.selectedPrediction && this.selectedImage) {
      this.getPrediction()
    }
  }

  validateNumbers() {
    /*
    Call validation methods for confidence interval and NMS
    */
    this.validateConfidence();
    this.validateIoU();
    this.validateScore();
    this.validateGroundTruthIoU();
  }

  validateConfidence() {
    /*
    Validate confidence interval so that min and max are valid ([0,100]) and min<max
    */
    if (this.predictionSettings.minConf == null)
      this.predictionSettings.minConf = 0
    if (this.predictionSettings.maxConf == null)
      this.predictionSettings.maxConf = 100
    this.predictionSettings.minConf = Math.max(0, this.predictionSettings.minConf);
    this.predictionSettings.maxConf = Math.min(this.predictionSettings.maxConf, 100);
    if (this.predictionSettings.minConf > this.predictionSettings.maxConf)
      this.predictionSettings.minConf = this.predictionSettings.maxConf;
  }

  validateIoU() {
    /*
    Validate IoU value so that it is valid ([0,1])
    */
    if (this.predictionSettings.nmsIoU == null)
      this.predictionSettings.nmsIoU = 0
    else if (this.predictionSettings.nmsIoU < 0)
      this.predictionSettings.nmsIoU = 0;
    else if (this.predictionSettings.nmsIoU > 1)
      this.predictionSettings.nmsIoU = 1;
  }

  validateScore() {
    /*
    Validate score value so that it is valid ([0,1])
    */
    if (this.predictionSettings.nmsScore == null)
      this.predictionSettings.nmsScore = 0
    else if (this.predictionSettings.nmsScore < 0)
      this.predictionSettings.nmsScore = 0;
    else if (this.predictionSettings.nmsScore > 1)
      this.predictionSettings.nmsScore = 1;
  }

  validateGroundTruthIoU() {
    /*
    Validate ground truth IoU value (used for overlapping) so that it is valid ([0,1])
    */
    if (this.predictionSettings.groundTruthIoU == null)
      this.predictionSettings.groundTruthIoU = 0
    else if (this.predictionSettings.groundTruthIoU < 0)
      this.predictionSettings.groundTruthIoU = 0;
    else if (this.predictionSettings.groundTruthIoU > 1)
      this.predictionSettings.groundTruthIoU = 1;
  }

}
