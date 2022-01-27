import {Component, OnInit} from '@angular/core';
import {ImageFile} from "./image-file";
import {ImageFilesService} from "./image-files.service";
import {ImageService} from "../image/image.service";
import {SelectedImageChangedService} from "../shared-services/selected-image-changed-service";
import {Subscription} from "rxjs";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";
import {DatasetFile} from "../dataset-list/dataset-file";

@Component({
  selector: 'app-image-files',
  templateUrl: './image-files.component.html',
  styleUrls: ['./image-files.component.css']
})
export class ImageFilesComponent implements OnInit {

  imageFiles: ImageFile[] = [];
  selectedDatasetChanged: Subscription;
  selectedImage!: string;

  constructor(private imageFilesService: ImageFilesService,
              private imageService: ImageService,
              private selectedImageChangedService: SelectedImageChangedService,
              private selectedDatasetChangedService: SelectedDatasetChangedService) {
    this.selectedDatasetChanged = this.selectedDatasetChangedService.newData.subscribe((data: DatasetFile) => {
      this.getImageFiles(data.name)
    })
  }

  ngOnInit() {
  }

  ngOnDestroy(): void {
    this.selectedDatasetChanged.unsubscribe();
  }

  getImageFiles(dataset: string): void {
    this.imageFilesService.getImageFiles(dataset)
      .subscribe((imageFiles: ImageFile[]) => {
        this.imageFiles = imageFiles
      })
  }

  onSelectedImageFileChanged($event: any) {
    this.selectedImage = $event.innerText;
    this.selectedImageChangedService.publish($event.innerText);
  }
}
