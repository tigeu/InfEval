import {Component, OnInit} from '@angular/core';
import {DatasetListService} from "./dataset-list.service";
import {Subscription} from "rxjs";
import {DatasetFile} from "./dataset-file";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";

@Component({
  selector: 'app-dataset-list',
  templateUrl: './dataset-list.component.html',
  styleUrls: ['./dataset-list.component.css']
})
export class DatasetListComponent implements OnInit {
  datasetList: DatasetFile[] = [];
  private datasetListSubscription: Subscription = new Subscription;

  constructor(private datasetListService: DatasetListService,
              private selectedDatasetChangedService: SelectedDatasetChangedService) {
    this.getDatasetList();
  }

  ngOnInit(): void {

  }

  ngOnDestroy(): void {
    this.datasetListSubscription.unsubscribe();
  }

  getDatasetList(): void {
    this.datasetListService.getDatasetList()
      .subscribe((datasetList: DatasetFile[]) => {
        this.datasetList = datasetList
      })
  }

  selectedDatasetChanged(dataset: string) {
    const selectedDataset = this.datasetList.find(x => x.name == dataset)
    if (selectedDataset)
      this.selectedDatasetChangedService.publish(selectedDataset);
  }
}
