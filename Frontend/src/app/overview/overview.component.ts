import {Component, OnInit} from '@angular/core';
import {OverviewService} from "./overview.service";
import {OverviewFile} from "./overview-file";
import {OverviewDatasetFile} from "./overview-dataset-file";
import {OverviewPredictionFile} from "./overview-prediction-file";
import {OverviewModelFile} from "./overview-model-file";
import {OverviewTaskFile} from "./overview-task-file";

@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.css']
})
export class OverviewComponent implements OnInit {
  datasetList: OverviewDatasetFile[] = [];
  predictionList: OverviewPredictionFile[] = [];
  modelList: OverviewModelFile[] = [];
  tasksList: OverviewTaskFile[] = [];

  deleting: boolean = false;

  constructor(private overviewService: OverviewService) {
  }

  ngOnInit(): void {
    this.getOverviewData();
  }

  getOverviewData(): void {
    this.overviewService.getOverviewData()
      .subscribe((overviewData: OverviewFile) => {
        this.datasetList = overviewData.datasets;
        this.predictionList = overviewData.predictions;
        this.modelList = overviewData.models;
        this.tasksList = overviewData.tasks;
      })
  }

  deleteDataset(name: string) {
    this.deleting = true;
    this.overviewService.deleteDataset(name)
      .subscribe(() => {
        this.deleting = false;
        this.getOverviewData();
      });
  }

  deletePrediction(name: string) {
    this.deleting = true;
    this.overviewService.deletePrediction(name)
      .subscribe(() => {
        this.deleting = false;
        this.getOverviewData();
      });
  }

  deleteModel(name: string) {
    this.deleting = true;
    this.overviewService.deleteModel(name)
      .subscribe(() => {
        this.deleting = false;
        this.getOverviewData();
      });
  }

  deleteTask(name: string) {
    this.deleting = true;
    this.overviewService.deleteTask(name)
      .subscribe(() => {
        this.deleting = false;
        this.getOverviewData();
      });
  }
}
