import {Component, OnInit} from '@angular/core';
import {ImageFile} from "./image-file";
import {ImageFilesService} from "./image-files.service";
import {ImageService} from "../image/image.service";
import {SelectedImageChangedService} from "../shared-services/selected-image-changed-service";
import {interval, Subscription} from "rxjs";

@Component({
  selector: 'app-image-files',
  templateUrl: './image-files.component.html',
  styleUrls: ['./image-files.component.css']
})
export class ImageFilesComponent implements OnInit {

  imageFiles: ImageFile[] = [];
  private imageFilesSubscription: Subscription = new Subscription;

  constructor(private imageFilesService: ImageFilesService,
              private imageService: ImageService,
              private selectedImageChangedService: SelectedImageChangedService) {
    this.getImageFiles();
  }

  ngOnInit(): void {
    this.imageFilesSubscription = interval(10000)
      .subscribe(
        intervalResponse => {
          this.getImageFiles();
        }
      );
  }

  ngOnDestroy(): void {
    this.imageFilesSubscription.unsubscribe()
  }

  getImageFiles(): void {
    this.imageFilesService.getImageFiles()
      .subscribe((imageFiles: ImageFile[]) => {
        this.imageFiles = imageFiles
      })
  }

  onSelectedImageFileChanged($event: MouseEvent) {
    const target = $event.target as HTMLElement;
    this.selectedImageChangedService.publish(target.innerText);
  }
}
