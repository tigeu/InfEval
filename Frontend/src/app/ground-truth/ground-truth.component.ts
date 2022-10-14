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
  /*
  Component that gets provides options for showing and filtering ground truth values for currently selected dataset.

  Attributes
  ----------
  groundTruthService : GroundTruthService
    Service for retrieving an image with drawn ground truth values
  selectedDatasetChangedService : SelectedDatasetChangedService
    Service for retrieving the selected dataset from a shared service
  selectedImageChangedService : SelectedImageChangedService
    Service for retrieving the selected image
  groundTruthChangedService : GroundTruthChangedService
    Service for publishing the retrieved image with drawn ground truth values
  selectedDatasetChanged : Subscription
    Subscription to retrieve currently selected dataset
  selectedDataset : DatasetFile
    Currently selected dataset
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
  groundTruthSettings : GroundTruthSettings
    Class for saving several different settings that are used to customize the drawings

  Methods
  -------
  getGroundTruth()
    Calls service to retrieve the ground truth drawings and publish the image
  setClassColors()
    Initialise showClasses and classColors values from currently selected dataset
  selectionChanged()
    Any setting was changed by user and a new image has to be requested
  */
  selectedDatasetChanged: Subscription;
  selectedDataset: DatasetFile = {name: ""};
  selectedImageChanged: Subscription;
  selectedImage: string = "";
  loading: boolean = false;
  showClasses: boolean[] = [];
  classColors: string[] = [];

  groundTruthSettings: GroundTruthSettings = {
    showGroundTruth: false,
    strokeSize: 2,
    showColored: true,
    showLabeled: true,
    fontSize: 10,
    classes: [],
    colors: []
  }

  constructor(private groundTruthService: GroundTruthService,
              private selectedDatasetChangedService: SelectedDatasetChangedService,
              private selectedImageChangedService: SelectedImageChangedService,
              private groundTruthChangedService: GroundTruthChangedService) {
    /*
    Initialise subscriptions for retrieving selected dataset and selected image

    Parameters
    ----------
    groundTruthService : GroundTruthService
      Service for retrieving an image with drawn ground truth values
    selectedDatasetChangedService : SelectedDatasetChangedService
      Service for retrieving the selected dataset from a shared service
    selectedImageChangedService : SelectedImageChangedService
      Service for retrieving the selected image
    groundTruthChangedService : GroundTruthChangedService
      Service for publishing the retrieved image with drawn ground truth values
    */
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
    /*
    Unsubscribe from all subscriptions
    */
    this.selectedImageChanged.unsubscribe();
    this.selectedDatasetChanged.unsubscribe();
  }

  getGroundTruth() {
    /*
    Calls service to retrieve the ground truth drawings and publish the image
    */
    this.loading = true;
    this.setClassColors();
    this.groundTruthService.getGroundTruth(this.selectedDataset.name, this.selectedImage, this.groundTruthSettings)
      .subscribe((groundTruth: GroundTruth) => {
        this.groundTruthChangedService.publish(groundTruth);
        this.loading = false;
      })
  }

  setClassColors() {
    /*
    Initialise showClasses and classColors values from currently selected dataset
    */
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
    /*
    Any setting was changed by user and a new image has to be requested
    */
    if (!this.groundTruthSettings.showGroundTruth)
      this.groundTruthChangedService.publish("");
    else if (this.selectedDataset && this.selectedImage) {
      this.getGroundTruth()
    }
  }
}
