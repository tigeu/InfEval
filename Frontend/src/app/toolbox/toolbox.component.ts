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

  downloadImageTriggered: Subscription;
  selectedImageChanged: Subscription;
  imageSelected: boolean = false;
  isDownloading: boolean = false;

  constructor(private downloadImageTriggeredService: DownloadImageTriggeredService,
              private selectedImageChangedService: SelectedImageChangedService,) {
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
    this.selectedImageChanged.unsubscribe();
  }

  async downloadTriggered() {
    if (!this.isDownloading) {
      this.isDownloading = true;
      await this.startDownload();
    }
  }

  async startDownload() {
    new Promise<void>((resolve) => {
      setTimeout(() => {
        this.downloadImageTriggeredService.publish(true);
        resolve();
      })
    })
  }
}
