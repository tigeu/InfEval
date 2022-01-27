import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {ImageService} from "./image.service";
import {SafeResourceUrl} from '@angular/platform-browser'
import {Image} from "./image";
import {Subscription} from "rxjs";
import {SelectedImageChangedService} from "../shared-services/selected-image-changed-service";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";
import {GroundTruthChangedService} from "../shared-services/ground-truth-changed.service";
import {PredictionChangedService} from "../shared-services/prediction-changed.service";
import {DatasetFile} from "../dataset-list/dataset-file";
import {DownloadImageTriggeredService} from "../shared-services/download-image-triggered.service";

@Component({
  selector: 'app-image',
  templateUrl: './image.component.html',
  styleUrls: ['./image.component.css']
})
export class ImageComponent implements OnInit {
  @ViewChild('downloadCanvas')
  downloadCanvas!: ElementRef<HTMLCanvasElement>;
  downloadLink: HTMLAnchorElement = document.createElement("a");

  selectedImageChanged: Subscription;
  selectedDatasetChanged: Subscription;
  groundTruthChanged: Subscription;
  predictionChanged: Subscription;
  downloadImageTriggered: Subscription;
  selectedDataset!: DatasetFile;

  image: Image = {file: new File([""], "")};
  imageUrl: SafeResourceUrl = "";

  groundTruthImage: Image = {file: new File([""], "")};
  groundTruthImageUrl: SafeResourceUrl = "";

  predictionImage: Image = {file: new File([""], "")};
  predictionImageUrl: SafeResourceUrl = "";

  constructor(private imageService: ImageService,
              private selectedImageChangedService: SelectedImageChangedService,
              private selectedDatasetChangedService: SelectedDatasetChangedService,
              private groundTruthChangedService: GroundTruthChangedService,
              private predictionChangedService: PredictionChangedService,
              private downloadImageTriggeredService: DownloadImageTriggeredService) {
    this.selectedImageChanged = this.selectedImageChangedService.newData.subscribe((data: any) => {
      this.resetImages();
      this.getImage(data);
    });
    this.selectedDatasetChanged = this.selectedDatasetChangedService.newData.subscribe((data: DatasetFile) => {
      this.resetImages();
      this.selectedDataset = data
    });
    this.groundTruthChanged = this.groundTruthChangedService.newData.subscribe((data: any) => {
      if (data)
        this.setGroundTruthImage(data);
      else
        this.resetGroundTruthImage();
    });
    this.predictionChanged = this.predictionChangedService.newData.subscribe((data: any) => {
      if (data)
        this.setPredictionImage(data);
      else
        this.resetPredictionImage();
    });
    this.downloadImageTriggered = this.downloadImageTriggeredService.newData.subscribe((data: any) => {
      if (data)
        this.downloadImage();
    });
  }

  ngOnInit(): void {
  }

  ngOnDestroy(): void {
    this.selectedImageChanged.unsubscribe();
    this.selectedDatasetChanged.unsubscribe();
    this.groundTruthChanged.unsubscribe();
    this.predictionChanged.unsubscribe();
    this.downloadImageTriggered.unsubscribe();
  }

  setImage(image: Image) {
    this.image = image
    this.imageUrl = 'data:image/jpg;base64,' + image["file"];
  }

  setGroundTruthImage(image: Image) {
    this.groundTruthImage = image
    this.groundTruthImageUrl = 'data:image/jpg;base64,' + image["file"];
  }

  setPredictionImage(image: Image) {
    this.predictionImage = image
    this.predictionImageUrl = 'data:image/jpg;base64,' + image["file"];
  }

  resetImages() {
    this.resetImage();
    this.resetGroundTruthImage();
    this.resetPredictionImage();
  }

  resetImage() {
    this.image = {file: new File([""], "")};
    this.imageUrl = "";
  }

  resetGroundTruthImage() {
    this.groundTruthImage = {file: new File([""], "")};
    this.groundTruthImageUrl = "";
  }

  resetPredictionImage() {
    this.predictionImage = {file: new File([""], "")};
    this.predictionImageUrl = "";
  }

  getImage(imageName: String): void {
    this.imageService.getImage(this.selectedDataset.name, imageName)
      .subscribe({
        next: this.setImage.bind(this),
        error: this.resetImages.bind(this)
      })
  }

  downloadImage() {
    let context = this.downloadCanvas.nativeElement.getContext('2d');
    if (context) {
      this.createImage(context)
      this.downloadLink.href = this.downloadCanvas.nativeElement.toDataURL();
      if (this.image.name)
        this.downloadLink.download = this.image.name;
      this.downloadLink.click();
    }
  }

  createImage(context: CanvasRenderingContext2D) {
    let img = new Image();
    img.src = this.imageUrl.toString()
    this.downloadCanvas.nativeElement.width = img.width;
    this.downloadCanvas.nativeElement.height = img.height;
    context.drawImage(img, 0, 0);
    img.src = this.groundTruthImageUrl.toString()
    context.drawImage(img, 0, 0);
    img.src = this.predictionImageUrl.toString()
    context.drawImage(img, 0, 0);
  }
}
