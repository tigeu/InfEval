import {Component, OnInit} from '@angular/core';
import {ImageFile} from "./ImageFile";
import {ImageFilesService} from "./image-files.service";
import {ImageService} from "../image/image.service";
import {SelectedImageChangedService} from "../SharedServices/SelectedImageChangedService";

@Component({
  selector: 'app-image-files',
  templateUrl: './image-files.component.html',
  styleUrls: ['./image-files.component.css']
})
export class ImageFilesComponent implements OnInit {

  imageFiles!: ImageFile[];

  constructor(private imageFilesService: ImageFilesService, private imageService: ImageService,
              private selectedImageChangedService: SelectedImageChangedService) {
  }

  ngOnInit(): void {
    this.getImageFiles();
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
