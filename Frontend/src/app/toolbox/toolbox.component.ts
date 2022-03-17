import {Component, OnInit} from '@angular/core';
import {DownloadImageTriggeredService} from "../shared-services/download-image-triggered.service";
import {Subscription} from "rxjs";
import {SelectedImageChangedService} from "../shared-services/selected-image-changed-service";

@Component({
  selector: 'app-toolbox',
  templateUrl: './toolbox.component.html',
  styleUrls: ['./toolbox.component.css']
})
export class ToolboxComponent implements OnInit {
  /*
  Component that contains GroundTruthComponent and PredictionsComponent. Also starts the download when triggered.

  Attributes
  ----------
  downloadImageTriggeredService : DownloadImageTriggeredService
    Service for retrieving the download triggered event
  selectedImageChangedService : SelectedImageChangedService
    Service for retrieving the selected image
  downloadImageTriggered : Subscription
    Subscription for retrieving the download triggered event
  selectedImageChanged : Subscription
    Subscription for retrieving the selected image
  imageSelected : boolean
    Indicating whether an image was selected
  isDownloading : boolean
    Indicating whether a download is currently being processed

  Methods
  -------
  downloadTriggered()
    Trigger download by sending information to image component
  startDownload()
    Start download by sending information to image component
  */
  downloadImageTriggered: Subscription;
  selectedImageChanged: Subscription;
  imageSelected: boolean = false;
  isDownloading: boolean = false;

  constructor(private downloadImageTriggeredService: DownloadImageTriggeredService,
              private selectedImageChangedService: SelectedImageChangedService) {
    /*
    Initialise subscriptions for retrieving triggered download and selected image

    Parameters
    ----------
    downloadImageTriggeredService : DownloadImageTriggeredService
      Service for retrieving the download triggered event
    selectedImageChangedService : SelectedImageChangedService
      Service for retrieving the selected image
    */
    this.downloadImageTriggered = this.downloadImageTriggeredService.newData.subscribe((data: boolean) => {
      if (!data) {
        this.isDownloading = false;
      }
    });
    this.selectedImageChanged = this.selectedImageChangedService.newData.subscribe((data: any) => {
      this.imageSelected = !!data;
    });
  }

  ngOnInit(): void {
  }

  ngOnDestroy(): void {
    /*
    Unsubscribe from all subscriptions
    */
    this.selectedImageChanged.unsubscribe();
  }

  async downloadTriggered() {
    /*
    Trigger download by sending information to image component
    */
    if (!this.isDownloading) {
      this.isDownloading = true;
      await this.startDownload();
    }
  }

  async startDownload() {
    /*
    Start download by sending information to image component
    */
    new Promise<void>((resolve) => {
      setTimeout(() => {
        this.downloadImageTriggeredService.publish(true);
        resolve();
      })
    })
  }
}
