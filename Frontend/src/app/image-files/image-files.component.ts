import {Component, OnInit} from '@angular/core';
import {ImageFile} from "./image-file";
import {ImageFilesService} from "./image-files.service";
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
  /*
  Component that gets a list of image file names for dataset from /image-files and displays them in a list. The selected
  image file name is sent to SelectedImageChangedService.

  Attributes
  ----------
  imageFilesService : ImageFilesService
    Service for retrieving a list of image file names
  selectedImageChangedService : SelectedImageChangedService
    Service for publishing the selected image file name
  selectedDatasetChangedService : SelectedDatasetChangedService
    Service for retrieving the selected dataset from a shared service
  imageFiles : ImageFile[]
    List of retrieved image file names
  filteredImageFiles : ImageFile[]
    List of filtered image files based if the text is contained in the file name
  selectedDatasetChanged : Subscription
    Subscription to retrieve currently selected dataset
  selectedImage : string
    Name of currently selected image file
  filterName : string
    Filter used for filtering file names

  Methods
  -------
  getImageFiles(dataset: string)
    Calls service to retrieve the list of image file names and save it to imageFiles
  onSelectedImageFileChanged($event: any)
    Sets the currently selected image and publishes it
  filterFiles(value: string)
    Filter files based on given string
  */
  imageFiles: ImageFile[] = [];
  filteredImageFiles: ImageFile[] = [];
  selectedDatasetChanged: Subscription;
  selectedImage!: string;
  filterName: string = "";

  constructor(private imageFilesService: ImageFilesService,
              private selectedImageChangedService: SelectedImageChangedService,
              private selectedDatasetChangedService: SelectedDatasetChangedService) {
    /*
    Initialise subscription for retrieving selected dataset

    Parameters
    ----------
    imageFilesService : ImageFilesService
      Service for retrieving a list of image file names
    selectedImageChangedService : SelectedImageChangedService
      Service for publishing the selected image file name
    selectedDatasetChangedService : SelectedDatasetChangedService
      Service for retrieving the selected dataset from a shared service
    */
    this.selectedDatasetChanged = this.selectedDatasetChangedService.newData.subscribe((data: DatasetFile) => {
      this.getImageFiles(data.name)
    })
  }

  ngOnInit() {
  }

  ngOnDestroy(): void {
    /*
    Unsubscribe from all subscriptions
    */
    this.selectedDatasetChanged.unsubscribe();
  }

  getImageFiles(dataset: string): void {
    /*
    Calls service to retrieve the list of image file names and save it to imageFiles

    Parameters
    ----------
    dataset : string
      Name of currently selected dataset
    */
    this.imageFilesService.getImageFiles(dataset)
      .subscribe((imageFiles: ImageFile[]) => {
        this.imageFiles = imageFiles
        this.filterFiles(this.filterName);
      })
  }

  onSelectedImageFileChanged($event: any) {
    /*
    Sets the currently selected image and publishes it

    Parameters
    ----------
    $event : any
      Click event with name of clicked element in it
    */
    this.selectedImage = $event.innerText;
    this.selectedImageChangedService.publish($event.innerText);
  }

  filterFiles(value: string) {
    /*
    Filter files based on given string

    Parameters
    ----------
    value : string
      Name which should be filtered
    */
    this.filterName = value;
    if (!value)
      this.filteredImageFiles = this.imageFiles;
    else
      this.filteredImageFiles = this.imageFiles.filter(file => file.name.toLowerCase().includes(value.toLowerCase()))
  }
}
