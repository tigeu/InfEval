import {Component, OnInit} from '@angular/core';
import {ImageService} from "./image.service";
import {DomSanitizer, SafeResourceUrl} from '@angular/platform-browser'
import {Image} from "./image";
import {Subscription} from "rxjs";
import {SelectedImageChangedService} from "../SharedServices/SelectedImageChangedService";

@Component({
  selector: 'app-image',
  templateUrl: './image.component.html',
  styleUrls: ['./image.component.css']
})
export class ImageComponent implements OnInit {

  mySubscription!: Subscription;

  image!: Image;
  imageUrl!: SafeResourceUrl;

  constructor(private imageService: ImageService, private domSanitizer: DomSanitizer,
              private selectedImageChangedService: SelectedImageChangedService) {
    this.mySubscription = this.selectedImageChangedService.newData.subscribe((data: any) => {
      this.getImage(data)
    })
  }

  getImage(imageName: String): void {
    this.imageService.getImage(imageName)
      .subscribe((image: Image) => {
        this.image = image
        this.imageUrl = 'data:image/jpg;base64,' + image["file"];
      })
  }

  ngOnInit(): void {
  }
}
