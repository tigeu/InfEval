import {Component, OnInit} from '@angular/core';
import {ImageService} from "./image.service";
import {DomSanitizer, SafeResourceUrl} from '@angular/platform-browser'
import {Image} from "./image";

@Component({
  selector: 'app-image',
  templateUrl: './image.component.html',
  styleUrls: ['./image.component.css']
})
export class ImageComponent implements OnInit {

  image!: Image;
  imageUrl!: SafeResourceUrl;

  constructor(private imageService: ImageService, private domSanitizer: DomSanitizer) {
  }

  getImage(imageName: String): void {
    this.imageService.getImage(imageName)
      .subscribe((image: Image) => {
        this.image = image
        this.imageUrl = 'data:image/jpg;base64,' + image["file"];
      })
  }

  ngOnInit(): void {
    this.getImage("2018_0714_112610_059.JPG"); // TODO remove when directory view is ready
  }

}
