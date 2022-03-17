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
  /*
  Component that gets the selected image from /image and displays it in the main view.

  Attributes
  ----------
  imageService : ImageService
    Service for retrieving the selected Image
  selectedImageChangedService : SelectedImageChangedService
    Service for retrieving the name of the selected image
  selectedDatasetChangedService : SelectedDatasetChangedService
    Service for retrieving the selected dataset from a shared service
  groundTruthChangedService : GroundTruthChangedService
    Service for retrieving the ground truth image from a shared service
  predictionChangedService : PredictionChangedService
    Service for retrieving the prediction image from a shared service
  downloadImageTriggeredService : DownloadImageTriggeredService
    Service for retrieving the information when download is triggered
  downloadCanvas : ElementRef<HTMLCanvasElement>
    Canvas in which all images are drawn so that they can be downloaded
  downloadLink : HTMLAnchorElement
    Link from which the image can be downloaded
  selectedImageChanged : Subscription
    Subscription to retrieve currently selected image name
  selectedDatasetChanges : Subscription
    Subscription to retrieve currently selected dataset
  groundTruthChanged : Subscription
    Subscription to retrieve current ground truth image
  predictionChanged : Subscription
    Subscription to retrieve current prediction image
  downloadImageTriggered : Subscription
    Subscription to retrieve when download is triggered
  selectedDataset : DatasetFile
    Currently selected Dataset
  image : Image
    Currently selected Image
  imageUrl : SafeResourceUrl
    Url to safely show image
  groundTruthImage : Image
    Currently selected ground truth image
  groundTruthImageUrl : SafeResourceUrl
    Url to safely show ground truth image
  predictionImage : Image
    Currently selected prediction image
  predictionImageUrl : SafeResourceUrl
    Url to safely prediction image

  Methods
  -------
  setImage(image : Image)
    Set currently selected image and according safe url
  setGroundTruthImage(image : Image)
    Set currently selected ground truth image and according safe url
  setPredictionImage(image : Image)
    Set currently selected prediction image and according safe url
  resetImages()
    Reset all images
  resetImage()
    Reset main image
  resetGroundTruthImage()
    Reset ground truth image
  resetPredictionImage()
    Reset prediction image
  getImage(imageName : string)
    Calls service to retrieve the current selected image
  downloadImage()
    Initiate drawing of images and provide download link
  createImage(context : CanvasRenderingContext2D)
    Draw all current images in canvas
  */
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
    /*
    Initialise subscriptions for retrieving selected image, dataset, ground truth, prediction and download trigger

    Parameters
    ----------
    imageService : ImageService
      Service for retrieving the selected Image
    selectedImageChangedService : SelectedImageChangedService
      Service for retrieving the name of the selected image
    selectedDatasetChangedService : SelectedDatasetChangedService
      Service for retrieving the selected dataset from a shared service
    groundTruthChangedService : GroundTruthChangedService
      Service for retrieving the ground truth image from a shared service
    predictionChangedService : PredictionChangedService
      Service for retrieving the prediction image from a shared service
    downloadImageTriggeredService : DownloadImageTriggeredService
      Service for retrieving the information when download is triggered
    */
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
    this.downloadImageTriggered = this.downloadImageTriggeredService.newData.subscribe((data: boolean) => {
      if (data)
        this.downloadImage();
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
    this.groundTruthChanged.unsubscribe();
    this.predictionChanged.unsubscribe();
    this.downloadImageTriggered.unsubscribe();
  }

  setImage(image: Image) {
    /*
    Set currently selected image and according safe url

    Parameters
    ----------
    image : string
      Currently selected image
    */
    this.image = image
    this.imageUrl = 'data:image/jpg;base64,' + image["file"];
  }

  setGroundTruthImage(image: Image) {
    /*
    Set currently selected ground truth image and according safe url

    Parameters
    ----------
    image : string
      Currently selected ground truth image
    */
    this.groundTruthImage = image
    this.groundTruthImageUrl = 'data:image/jpg;base64,' + image["file"];
  }

  setPredictionImage(image: Image) {
    /*
    Set currently selected prediction image and according safe url

    Parameters
    ----------
    image : string
      Currently selected prediction image
    */
    this.predictionImage = image
    this.predictionImageUrl = 'data:image/jpg;base64,' + image["file"];
  }

  resetImages() {
    /*
    Reset all images
    */
    this.resetImage();
    this.resetGroundTruthImage();
    this.resetPredictionImage();
  }

  resetImage() {
    /*
    Reset main image
    */
    this.image = {file: new File([""], "")};
    this.imageUrl = "";
  }

  resetGroundTruthImage() {
    /*
    Reset ground truth image
    */
    this.groundTruthImage = {file: new File([""], "")};
    this.groundTruthImageUrl = "";
  }

  resetPredictionImage() {
    /*
    Reset prediction image
    */
    this.predictionImage = {file: new File([""], "")};
    this.predictionImageUrl = "";
  }

  getImage(imageName: string): void {
    /*
    Calls service to retrieve the current selected image

    Parameters
    ----------
    imageName : string
      Name of currently selected image
    */
    this.imageService.getImage(this.selectedDataset.name, imageName)
      .subscribe({
        next: this.setImage.bind(this),
        error: this.resetImages.bind(this)
      })
  }

  downloadImage() {
    /*
    Initiate drawing of images and provide download link
    */
    let context = this.downloadCanvas.nativeElement.getContext('2d');
    if (context) {
      this.createImage(context)
      this.downloadLink.href = this.downloadCanvas.nativeElement.toDataURL();
      if (this.image.name)
        this.downloadLink.download = this.image.name;
      this.downloadLink.click();
    }
    this.downloadImageTriggeredService.publish(false);
  }

  createImage(context: CanvasRenderingContext2D) {
    /*
    Draw all current images in canvas
    */
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
