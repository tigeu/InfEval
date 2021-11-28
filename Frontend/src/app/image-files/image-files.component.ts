import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {ImageFile} from "./ImageFile";
import {ImageFilesService} from "./image-files.service";
import {ImageService} from "../image/image.service";

@Component({
  selector: 'app-image-files',
  templateUrl: './image-files.component.html',
  styleUrls: ['./image-files.component.css']
})
export class ImageFilesComponent implements OnInit {

  @Output()
  onSelectedImageChanged: EventEmitter<any> = new EventEmitter<any>();

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

  onSelectedImageFileChanged($event: MouseEvent) {
    const target = $event.target as HTMLElement;
    this.onSelectedImageChanged.emit(target.innerText);
  }
}
