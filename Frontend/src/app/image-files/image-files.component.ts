import {Component, OnInit} from '@angular/core';
import {ImageFile} from "./ImageFile";
import {ImageFilesService} from "./image-files.service";
import {ImageService} from "../image/image.service";

@Component({
  selector: 'app-files',
  templateUrl: './image-files.component.html',
  styleUrls: ['./image-files.component.css']
})
export class ImageFilesComponent implements OnInit {

  imageFiles!: ImageFile[];

  constructor(private imageFilesService: ImageFilesService, private imageService: ImageService) {
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
}
