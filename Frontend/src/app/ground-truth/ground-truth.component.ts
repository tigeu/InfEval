import {Component, OnInit} from '@angular/core';
import {GroundTruthService} from "./ground-truth.service";
import {GroundTruthSettings} from "./ground-truth-settings";
import {SelectedImageChangedService} from "../shared-services/selected-image-changed-service";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";
import {Subscription} from "rxjs";
import {GroundTruthChangedService} from "../shared-services/ground-truth-changed.service";
import {GroundTruth} from "./ground-truth";

@Component({
  selector: 'app-ground-truth',
  templateUrl: './ground-truth.component.html',
  styleUrls: ['./ground-truth.component.css']
})
export class GroundTruthComponent implements OnInit {
  selectedDatasetChanged: Subscription;
  selectedDataset: string = "";
  selectedImageChanged: Subscription;
  selectedImage: string = "";

  groundTruthSettings: GroundTruthSettings = {
    showGroundTruth: false,
    strokeSize: 10,
    showColored: true,
    showLabeled: true,
    fontSize: 35
  }

  constructor(private groundTruthService: GroundTruthService,
              private selectedDatasetChangedService: SelectedDatasetChangedService,
              private selectedImageChangedService: SelectedImageChangedService,
              private groundTruthChangedService: GroundTruthChangedService) {
    this.selectedDatasetChanged = this.selectedDatasetChangedService.newData.subscribe((data: string) => {
      this.selectedDataset = data
    })
    this.selectedImageChanged = this.selectedImageChangedService.newData.subscribe((data: any) => {
      this.selectedImage = data;
      this.groundTruthSettings.showGroundTruth = false;
    });
  }

  ngOnInit(): void {
  }

  selectionChanged() {
    if (!this.groundTruthSettings.showGroundTruth)
      this.groundTruthChangedService.publish("");
    else if (this.selectedDataset && this.selectedImage) {
      this.groundTruthService.getGroundTruth(this.selectedDataset, this.selectedImage, this.groundTruthSettings)
        .subscribe((groundTruth: GroundTruth) => {
          this.groundTruthChangedService.publish(groundTruth);
        })
    }
  }
}
