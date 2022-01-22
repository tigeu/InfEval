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

  selectedImageChanged: Subscription;
  imageSelected: boolean = false;

  constructor(private downloadImageTriggeredService: DownloadImageTriggeredService,
              private selectedImageChangedService: SelectedImageChangedService,) {
    this.selectedImageChanged = this.selectedImageChangedService.newData.subscribe((data: any) => {
      this.imageSelected = !!data;
    });
  }

  ngOnInit(): void {
  }

  downloadTriggered() {
    this.downloadImageTriggeredService.publish(true);
  }
}
