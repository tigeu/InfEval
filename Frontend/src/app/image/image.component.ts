import {Component, OnInit} from '@angular/core';
import {ImageService} from "./image.service";
import {SafeResourceUrl} from '@angular/platform-browser'
import {Image} from "./image";
import {Subscription} from "rxjs";
import {SelectedImageChangedService} from "../shared-services/selected-image-changed-service";

@Component({
  selector: 'app-image',
  templateUrl: './image.component.html',
  styleUrls: ['./image.component.css']
})
export class ImageComponent implements OnInit {

  selectedImageChanged: Subscription;

  image: Image = {file: new File([""], "")};
  imageUrl: SafeResourceUrl = "";

  constructor(private imageService: ImageService, private selectedImageChangedService: SelectedImageChangedService) {
    this.selectedImageChanged = this.selectedImageChangedService.newData.subscribe((data: any) => {
      this.getImage(data)
    })
  }

  setImage(image: Image) {
    this.image = image
    this.imageUrl = 'data:image/jpg;base64,' + image["file"];
  }

  resetImage() {
    this.image = {file: new File([""], "")};
    this.imageUrl = "";
  }

  getImage(imageName: String): void {
    this.imageService.getImage(imageName)
      .subscribe({
        next: this.setImage.bind(this),
        error: this.resetImage.bind(this)
      })
  }

  ngOnInit(): void {
  }
}
