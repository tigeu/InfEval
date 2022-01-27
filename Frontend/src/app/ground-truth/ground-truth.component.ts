import {Component, OnInit} from '@angular/core';
import {GroundTruthService} from "./ground-truth.service";
import {GroundTruthSettings} from "./ground-truth-settings";
import {SelectedImageChangedService} from "../shared-services/selected-image-changed-service";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";
import {Subscription} from "rxjs";
import {GroundTruthChangedService} from "../shared-services/ground-truth-changed.service";
import {GroundTruth} from "./ground-truth";
import {DatasetFile} from "../dataset-list/dataset-file";

@Component({
  selector: 'app-ground-truth',
  templateUrl: './ground-truth.component.html',
  styleUrls: ['./ground-truth.component.css']
})
export class GroundTruthComponent implements OnInit {
  selectedDatasetChanged: Subscription;
  selectedDataset: DatasetFile = {'name': ""};
  selectedImageChanged: Subscription;
  selectedImage: string = "";
  loading: boolean = false;
  showClasses: boolean[] = [];
  classColors: string[] = [];

  groundTruthSettings: GroundTruthSettings = {
    showGroundTruth: false,
    strokeSize: 10,
    showColored: true,
    showLabeled: true,
    fontSize: 35,
    classes: [],
    colors: []
  }

  constructor(private groundTruthService: GroundTruthService,
              private selectedDatasetChangedService: SelectedDatasetChangedService,
              private selectedImageChangedService: SelectedImageChangedService,
              private groundTruthChangedService: GroundTruthChangedService) {
    this.selectedDatasetChanged = this.selectedDatasetChangedService.newData.subscribe((data: DatasetFile) => {
      this.selectedDataset = data;
      this.selectedImage = "";
      this.groundTruthSettings.showGroundTruth = false;
      if (data.classes && data.colors) {
        this.showClasses = new Array(data.classes.length).fill(true);
        this.classColors = data.colors;
      }
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
  }

  getGroundTruth() {
    this.loading = true;
    this.setClassColors();
    this.groundTruthService.getGroundTruth(this.selectedDataset.name, this.selectedImage, this.groundTruthSettings)
      .subscribe((groundTruth: GroundTruth) => {
        this.groundTruthChangedService.publish(groundTruth);
        this.loading = false;
      })
  }

  setClassColors() {
    if (this.selectedDataset.classes) {
      let classes: string[] = [];
      let colors: string[] = [];
      for (let i = 0; i < this.selectedDataset.classes?.length; i++) {
        if (this.showClasses[i]) {
          classes.push(this.selectedDataset.classes[i]);
          colors.push(this.classColors[i]);
        }
      }
      this.groundTruthSettings.classes = classes;
      this.groundTruthSettings.colors = colors;
    }
  }

  selectionChanged() {
    if (!this.groundTruthSettings.showGroundTruth)
      this.groundTruthChangedService.publish("");
    else if (this.selectedDataset && this.selectedImage) {
      this.getGroundTruth()
    }
  }
}
