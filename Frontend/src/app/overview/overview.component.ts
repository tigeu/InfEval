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
  /*
  Component that gets lists of datasets, predictions, models and tasks with all relevant information and displays it in
  different tables. Also allows to delete entries.

  Attributes
  ----------
  overviewService : OverviewService
    Service for retrieving all lists
  datasetList : OverviewDatasetFile[]
    List of datasets with all relevant information
  predictionList : OverviewPredictionFile[]
    List of predictions with all relevant information
  modelList : OverviewModelFile[]
    List of models with all relevant information
  tasksList : OverviewTaskFile[]
    List of tasks with all relevant information
  deleting : boolean
    Indicates whether delete is currently in process

  Methods
  -------
  getOverviewData()
    Calls service to retrieve all lists and extract them
  deleteDataset(name: string)
    Call service to delete dataset with given name
  deletePrediction(name: string)
    Call service to delete prediction with given name
  deleteModel(name: string)
    Call service to delete model with given name
  deleteTask(name: string)
    Call service to delete task with given name
  */
  datasetList: OverviewDatasetFile[] = [];
  predictionList: OverviewPredictionFile[] = [];
  modelList: OverviewModelFile[] = [];
  tasksList: OverviewTaskFile[] = [];

  deleting: boolean = false;

  constructor(private overviewService: OverviewService) {
    /*
    Retrieve all lists

    Parameters
    ----------
    overviewService : OverviewService
      Service for retrieving all lists
    */
    this.getOverviewData();
  }

  ngOnInit(): void {
  }

  getOverviewData(): void {
    /*
    Calls service to retrieve all lists and extract them
    */
    this.overviewService.getOverviewData()
      .subscribe((overviewData: OverviewFile) => {
        this.datasetList = overviewData.datasets;
        this.predictionList = overviewData.predictions;
        this.modelList = overviewData.models;
        this.tasksList = overviewData.tasks;
      })
  }

  deleteDataset(name: string) {
    /*
    Call service to delete dataset with given name

    Parameters
    ----------
    name : string
      Name of dataset that should be deleted
    */
    this.deleting = true;
    this.overviewService.deleteDataset(name)
      .subscribe(() => {
        this.deleting = false;
        this.getOverviewData();
      });
  }

  deletePrediction(name: string) {
    /*
    Call service to delete prediction with given name

    Parameters
    ----------
    name : string
      Name of prediction that should be deleted
    */
    this.deleting = true;
    this.overviewService.deletePrediction(name)
      .subscribe(() => {
        this.deleting = false;
        this.getOverviewData();
      });
  }

  deleteModel(name: string) {
    /*
    Call service to delete model with given name

    Parameters
    ----------
    name : string
      Name of model that should be deleted
    */
    this.deleting = true;
    this.overviewService.deleteModel(name)
      .subscribe(() => {
        this.deleting = false;
        this.getOverviewData();
      });
  }

  deleteTask(name: string) {
    /*
    Call service to delete task with given name

    Parameters
    ----------
    name : string
      Name of task that should be deleted
    */
    this.deleting = true;
    this.overviewService.deleteTask(name)
      .subscribe(() => {
        this.deleting = false;
        this.getOverviewData();
      });
  }
}
