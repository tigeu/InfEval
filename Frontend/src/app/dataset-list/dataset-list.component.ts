import {Component, OnInit} from '@angular/core';
import {DatasetListService} from "./dataset-list.service";
import {DatasetFile} from "./dataset-file";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";

@Component({
  selector: 'app-dataset-list',
  templateUrl: './dataset-list.component.html',
  styleUrls: ['./dataset-list.component.css']
})
export class DatasetListComponent implements OnInit {
  /*
  Component that gets a list of datasets from /dataset-list and displays them in a dropdown menu. Selected dataset is
  sent to SelectedDatasetChangedService.

  Attributes
  ----------
  datasetListService : DatasetListService
    Service for retrieving a list of datasets
  selectedDatasetChangedService : SelectedDatasetChangedService
    Service for publishing the selected dataset
  datasetList : DatasetFile[]
    List of retrieved datasets

  Methods
  -------
  getDatasetList()
    Calls service to retrieve the dataset list and save it to datasetList
  selectedDatasetChanged(dataset: string)
    Finds the selected dataset and publishes it using a shared service
  */
  datasetList: DatasetFile[] = [];

  constructor(private datasetListService: DatasetListService,
              private selectedDatasetChangedService: SelectedDatasetChangedService) {
    /*
    Retrieve list of datasets

    Parameters
    ----------
    datasetListService : DatasetListService
      Service for retrieving a list of datasets
    selectedDatasetChangedService : SelectedDatasetChangedService
      Service for publishing the selected dataset
    */
    this.getDatasetList();
  }

  ngOnInit(): void {
  }

  getDatasetList(): void {
    /*
    Calls service to retrieve the dataset list and save it to datasetList
    */
    this.datasetListService.getDatasetList()
      .subscribe((datasetList: DatasetFile[]) => {
        this.datasetList = datasetList
      })
  }

  selectedDatasetChanged(dataset: string) {
    /*
    Finds the selected dataset and publishes it using a shared service

    Parameters
    ----------
    dataset : string
      Name of selected dataset
    */
    const selectedDataset = this.datasetList.find(x => x.name == dataset)
    if (selectedDataset)
      this.selectedDatasetChangedService.publish(selectedDataset);
  }
}
