import {ComponentFixture, TestBed} from '@angular/core/testing';

import {ImageComponent} from './image.component';
import {HttpClientModule} from "@angular/common/http";
import {SelectedImageChangedService} from "../shared-services/selected-image-changed-service";
import {of} from "rxjs";
import {Image} from "./image";
import {ImageService} from "./image.service";
import {By} from "@angular/platform-browser";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";
import {GroundTruthChangedService} from "../shared-services/ground-truth-changed.service";
import {PredictionChangedService} from "../shared-services/prediction-changed.service";
import {DownloadImageTriggeredService} from "../shared-services/download-image-triggered.service";

describe('ImageComponent', () => {
  let component: ImageComponent;
  let fixture: ComponentFixture<ImageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
      ],
      providers: [
        SelectedImageChangedService,
      ],
      declarations: [
        ImageComponent,
      ]
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ImageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#getImage should change image', () => {
    const newImage: Image = {file: new File([""], "test_image.jpg")};
    const fakeImage: Image = {file: new File(["an"], "other_image.jpg")};
    const imageService = TestBed.inject(ImageService);
    spyOn(imageService, 'getImage').and.returnValue(of(newImage));
    component.selectedDataset = {name: "test_dataset"}

    component.getImage("test_image.jpg");

    expect(component.image).toBe(newImage);
    expect(component.image).not.toBe(fakeImage)
  });

  it('#getImage should change imageUrl', () => {
    const newImage: Image = {file: new File([""], "test_image.jpg")};
    const imageService = TestBed.inject(ImageService);

    component.selectedDataset = {name: "test_dataset"};
    spyOn(imageService, 'getImage').withArgs("test_dataset", "test_image.jpg").and.returnValue(of(newImage));

    component.getImage("test_image.jpg");

    expect(component.imageUrl).toBe('data:image/jpg;base64,' + newImage["file"]);
  });

  it('image subscription should trigger #getimage and #resetImages', () => {
    const selectedImageChangedService = TestBed.inject(SelectedImageChangedService);
    const spy = spyOn(component, 'getImage');
    const gtSpy = spyOn(component, 'resetImages');

    selectedImageChangedService.publish("test_image.jpg");

    expect(spy).toHaveBeenCalledWith("test_image.jpg");
    expect(gtSpy).toHaveBeenCalled();
  });

  it('gtimage subscription should trigger #setGroundTruthImage if data given', () => {
    const groundTruthChangedService = TestBed.inject(GroundTruthChangedService);
    const spy = spyOn(component, 'setGroundTruthImage');
    const newImage: Image = {file: new File([""], "test_image.jpg")};

    groundTruthChangedService.publish(newImage);

    expect(spy).toHaveBeenCalledWith(newImage);
  });

  it('gtimage subscription should trigger #resetGroundTruthImage if no data given', () => {
    const groundTruthChangedService = TestBed.inject(GroundTruthChangedService);
    const spy = spyOn(component, 'resetGroundTruthImage');

    groundTruthChangedService.publish("");

    expect(spy).toHaveBeenCalled();
  });

  it('predimage subscription should trigger #setPredictionImage if data given', () => {
    const predictionChangedService = TestBed.inject(PredictionChangedService);
    const spy = spyOn(component, 'setPredictionImage');
    const newImage: Image = {file: new File([""], "test_image.jpg")};

    predictionChangedService.publish(newImage);

    expect(spy).toHaveBeenCalledWith(newImage);
  });

  it('predimage subscription should trigger #resetPrediction if no data given', () => {
    const predictionChangedService = TestBed.inject(PredictionChangedService);
    const spy = spyOn(component, 'resetPredictionImage');

    predictionChangedService.publish("");

    expect(spy).toHaveBeenCalled();
  });


  it('dataset subscription should update selectedDataset and trigger #resetImages', () => {
    const selectedDatasetChangedService = TestBed.inject(SelectedDatasetChangedService);
    const spy = spyOn(component, 'resetImages');
    const dataset = {name: "test_dataset"}

    selectedDatasetChangedService.publish(dataset);

    expect(component.selectedDataset).toEqual(dataset);
    expect(spy).toHaveBeenCalled();
  });

  it('download subscription should initiate download if data', () => {
    const downloadImageTriggeredService = TestBed.inject(DownloadImageTriggeredService);
    const spy = spyOn(component, 'downloadImage');

    downloadImageTriggeredService.publish(true);

    expect(spy).toHaveBeenCalled();
  });

  it('download subscription should not initiate download if no data', () => {
    const downloadImageTriggeredService = TestBed.inject(DownloadImageTriggeredService);
    const spy = spyOn(component, 'downloadImage');

    downloadImageTriggeredService.publish(false);

    expect(spy).not.toHaveBeenCalled();
  });

  it('should not render image if image is undefined or null', () => {
    expect(fixture.debugElement.query(By.css('#selected-image'))).toBeNull();
  });

  it('should render image if image given', () => {
    const newImage: Image = {file: new File([""], "test_image1.jpg")};
    const imageService = TestBed.inject(ImageService);
    component.selectedDataset = {name: "test_dataset"}

    spyOn(imageService, 'getImage').withArgs("test_dataset", "test_image1.jpg").and.returnValue(of(newImage));

    component.getImage("test_image1.jpg");

    expect(component.imageUrl).toBeTruthy();
    fixture.detectChanges();
    expect(fixture.debugElement.query(By.css('#selected-image')).nativeElement.src).toBeTruthy();
  });

  it('should not render selected-ground-truth-image if image is undefined or null', () => {
    expect(fixture.debugElement.query(By.css('#selected-ground-truth-image'))).toBeNull();
  });

  it('should render image if ground truth image given', () => {
    const newImage: Image = {file: new File([""], "test_image.jpg")};
    const imageService = TestBed.inject(ImageService);

    component.selectedDataset = {name: "test_dataset"};

    spyOn(imageService, 'getImage').withArgs("test_dataset", "test_image.jpg").and.returnValue(of(newImage));

    component.setGroundTruthImage(newImage);

    expect(component.groundTruthImageUrl).toBeTruthy();
    fixture.detectChanges();
    expect(fixture.debugElement.query(By.css('#selected-ground-truth-image')).nativeElement.src).toBeTruthy();
  });

  it('should not render selected-prediction-image if image is undefined or null', () => {
    expect(fixture.debugElement.query(By.css('#selected-prediction-image'))).toBeNull();
  });

  it('should render image if prediction image given', () => {
    const newImage: Image = {file: new File([""], "test_image.jpg")};
    const imageService = TestBed.inject(ImageService);

    component.selectedDataset = {name: "test_dataset"}

    spyOn(imageService, 'getImage').withArgs("test_dataset", "test_image.jpg").and.returnValue(of(newImage));

    component.setPredictionImage(newImage);

    expect(component.predictionImageUrl).toBeTruthy();
    fixture.detectChanges();
    expect(fixture.debugElement.query(By.css('#selected-prediction-image')).nativeElement.src).toBeTruthy();
  });

  it('#resetImage should reset image', () => {
    component.resetImage();

    expect(component.image).toEqual({file: new File([""], "")});
    expect(component.imageUrl).toBe("");
  });

  it('#resetGroundTruthImage should reset image', () => {
    component.resetGroundTruthImage();

    expect(component.groundTruthImage).toEqual({file: new File([""], "")});
    expect(component.groundTruthImageUrl).toBe("");
  });

  it('#resetPredicitonImage should reset image', () => {
    component.resetPredictionImage();

    expect(component.predictionImage).toEqual({file: new File([""], "")});
    expect(component.predictionImageUrl).toBe("");
  });

  it('#resetImages should trigger reset methods', () => {
    const imageSpy = spyOn(component, 'resetImage');
    const groundTruthSpy = spyOn(component, 'resetGroundTruthImage');
    const predictionSpy = spyOn(component, 'resetPredictionImage');

    component.resetImages();

    expect(imageSpy).toHaveBeenCalled();
    expect(groundTruthSpy).toHaveBeenCalled();
    expect(predictionSpy).toHaveBeenCalled();
  });

  it('#downloadImage should trigger createImage and click on link', () => {
    const spy = spyOn(component, 'createImage');
    const linkSpy = spyOn(component.downloadLink, 'click');
    component.image.name = "test_name";

    component.downloadImage();

    expect(spy).toHaveBeenCalled();
    expect(linkSpy).toHaveBeenCalled();
  });

  it('#createImage should draw 3 images on canvas', () => {
    const context = component.downloadCanvas.nativeElement.getContext('2d');
    if (context) {
      const canvasSpy = spyOn(context, 'drawImage');

      component.createImage(context);

      expect(canvasSpy).toHaveBeenCalledTimes(3);
    } else {
      throw new Error("context can not be fetched")
    }
  });
});
