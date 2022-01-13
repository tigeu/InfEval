import {Component, OnInit} from '@angular/core';
import {ImageService} from "./image.service";
import {SafeResourceUrl} from '@angular/platform-browser'
import {Image} from "./image";
import {Subscription} from "rxjs";
import {SelectedImageChangedService} from "../shared-services/selected-image-changed-service";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";
import {GroundTruthChangedService} from "../shared-services/ground-truth-changed.service";

@Component({
  selector: 'app-image',
  templateUrl: './image.component.html',
  styleUrls: ['./image.component.css']
})
export class ImageComponent implements OnInit {

  selectedImageChanged: Subscription;
  selectedDatasetChanged: Subscription;
  groundTruthChanged: Subscription;
  selectedDataset!: string;

  image: Image = {file: new File([""], "")};
  imageUrl: SafeResourceUrl = "";

  groundTruthImage: Image = {file: new File([""], "")};
  groundTruthImageUrl: SafeResourceUrl = "";

  constructor(private imageService: ImageService,
              private selectedImageChangedService: SelectedImageChangedService,
              private selectedDatasetChangedService: SelectedDatasetChangedService,
              private groundTruthChangedService: GroundTruthChangedService) {
    this.selectedImageChanged = this.selectedImageChangedService.newData.subscribe((data: any) => {
      this.getImage(data)
      this.resetGroundTruthImage()
    });
    this.selectedDatasetChanged = this.selectedDatasetChangedService.newData.subscribe((data: string) => {
      this.selectedDataset = data
    });
    this.groundTruthChanged = this.groundTruthChangedService.newData.subscribe((data: any) => {
      if (data)
        this.setGroundTruthImage(data)
      else
        this.resetGroundTruthImage()
    });
  }

  setImage(image: Image) {
    this.image = image
    this.imageUrl = 'data:image/jpg;base64,' + image["file"];
  }

  setGroundTruthImage(image: Image) {
    this.groundTruthImage = image
    this.groundTruthImageUrl = 'data:image/jpg;base64,' + image["file"];
  }

  resetImage() {
    this.image = {file: new File([""], "")};
    this.imageUrl = "";
  }

  resetGroundTruthImage() {
    this.groundTruthImage = {file: new File([""], "")};
    this.groundTruthImageUrl = "";
  }

  getImage(imageName: String): void {
    this.imageService.getImage(this.selectedDataset, imageName)
      .subscribe({
        next: this.setImage.bind(this),
        error: this.resetImage.bind(this)
      })
  }

  ngOnInit(): void {
  }
}
