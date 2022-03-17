import {Component, Input, OnInit} from '@angular/core';
import {Subscription} from "rxjs";
import {PredictionFile} from "./prediction-file";
import {PredictionListService} from "./prediction-list.service";
import {SelectedPredictionChangedService} from "../shared-services/selected-prediction-changed.service";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";
import {DatasetFile} from "../dataset-list/dataset-file";

@Component({
  selector: 'app-prediction-list',
  templateUrl: './prediction-list.component.html',
  styleUrls: ['./prediction-list.component.css']
})
export class PredictionListComponent implements OnInit {
  /*
  Component that gets a list of predictions from /prediction-list and displays them in a dropdown menu. Selected
  prediction is sent to SelectedPredictionChangedService.

  Attributes
  ----------
  predictionListService : PredictionListService
    Service for retrieving a list of predictions
  selectedPredictionChangedService : SelectedPredictionChangedService
    Service for publishing the selected prediction
  selectedDatasetChangedService : SelectedDatasetChangedService
    Service for retrieving the selected dataset from a shared service
  predictionList : PredictionFile[]
    List of retrieved predictions
  selectedDataset : DatasetFile
    Currently selected dataset
  selectedDatasetChanged : Subscription
    Subscription to retrieve currently selected dataset

  Methods
  -------
  getPredictionList(dataset: string)
    Calls service to retrieve the prediction list and save it to predictionList
  selectedPredictionChanged(prediction: string)
    Finds the selected prediction and publishes it using a shared service
  */
  predictionList: PredictionFile[] = [];
  @Input() selectedDataset!: DatasetFile;
  selectedDatasetChanged: Subscription;

  constructor(private predictionListService: PredictionListService,
              private selectedPredictionChangedService: SelectedPredictionChangedService,
              private selectedDatasetChangedService: SelectedDatasetChangedService) {
    /*
    Initialise subscriptions for retrieving selected dataset

    Parameters
    ----------
    predictionListService : PredictionListService
      Service for retrieving a list of predictions
    selectedPredictionChangedService : SelectedPredictionChangedService
      Service for publishing the selected prediction
    selectedDatasetChangedService : SelectedDatasetChangedService
      Service for retrieving the selected dataset from a shared service
    */
    this.selectedDatasetChanged = this.selectedDatasetChangedService.newData.subscribe((data: DatasetFile) => {
      this.selectedDataset = data;
    })
  }

  ngOnInit(): void {
    /*
    Retrieve list of predictions
    */
    this.getPredictionList(this.selectedDataset.name)
  }

  getPredictionList(dataset: string): void {
    /*
    Calls service to retrieve the prediction list and save it to predictionList

    Parameters
    ----------
    dataset : string
      Name of currently selected dataset
    */
    this.predictionListService.getPredictionList(dataset)
      .subscribe((predictionList: PredictionFile[]) => {
        this.predictionList = predictionList
      })
  }

  selectedPredictionChanged(prediction: string) {
    /*
    Finds the selected prediction and publishes it using a shared service

    Parameters
    ----------
    prediction : string
      Name of selected prediction
    */
    const selectedPrediction = this.predictionList.find(x => x.name == prediction)
    if (selectedPrediction)
      this.selectedPredictionChangedService.publish(selectedPrediction);
  }
}
