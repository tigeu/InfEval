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
  predictionList: PredictionFile[] = [];
  private predictionListSubscription: Subscription = new Subscription;
  @Input() selectedDataset!: DatasetFile;
  selectedDatasetChanged: Subscription;

  constructor(private predictionListService: PredictionListService,
              private selectedPredictionChangedService: SelectedPredictionChangedService,
              private selectedDatasetChangedService: SelectedDatasetChangedService) {
    this.selectedDatasetChanged = this.selectedDatasetChangedService.newData.subscribe((data: DatasetFile) => {
      this.selectedDataset = data
    })
  }

  ngOnInit(): void {
    this.getPredictionList(this.selectedDataset.name)
  }

  ngOnDestroy(): void {
    this.predictionListSubscription.unsubscribe();
  }

  getPredictionList(dataset: string): void {
    this.predictionListService.getPredictionList(dataset)
      .subscribe((predictionList: PredictionFile[]) => {
        this.predictionList = predictionList
      })
  }

  selectedPredictionChanged(prediction: string) {
    this.selectedPredictionChangedService.publish(prediction);
  }
}
