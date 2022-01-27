import {ComponentFixture, TestBed} from '@angular/core/testing';

import {GroundTruthComponent} from './ground-truth.component';
import {HttpClientModule} from "@angular/common/http";
import {of} from "rxjs";
import {GroundTruthService} from "./ground-truth.service";
import {GroundTruthChangedService} from "../shared-services/ground-truth-changed.service";
import {GroundTruth} from "./ground-truth";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";
import {SelectedImageChangedService} from "../shared-services/selected-image-changed-service";

describe('GroundTruthComponent', () => {
  let component: GroundTruthComponent;
  let fixture: ComponentFixture<GroundTruthComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
      ],
      declarations: [GroundTruthComponent]
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GroundTruthComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#getGroundTruth trigger setClassColors and should publish image', () => {
      const groundTruth: GroundTruth = {file: new File([""], "test_image.jpg")};
      const groundTruthService = TestBed.inject(GroundTruthService);
      const groundTruthChangedService = TestBed.inject(GroundTruthChangedService);
      spyOn(groundTruthService, 'getGroundTruth').and.returnValue(of(groundTruth));
      const colorSpy = spyOn(component, "setClassColors");
      const spy = spyOn(groundTruthChangedService, 'publish');

      component.selectedDataset = {name: "test_dataset"};
      component.selectedImage = "test_image.jpg";

      component.getGroundTruth();

      expect(colorSpy).toHaveBeenCalled();
      expect(spy).toHaveBeenCalledWith(groundTruth)
    }
  );

  it('dataset subscription should set selectedDataset, init classes and colors, reset image and show selection', () => {
    const selectedDatasetChangedService = TestBed.inject(SelectedDatasetChangedService);
    const dataset = {name: "test_dataset", classes: ["class1", "class2"], colors: ["color1", "color2"]};

    selectedDatasetChangedService.publish(dataset)

    expect(component.selectedDataset).toEqual(dataset);
    expect(component.selectedImage).toEqual("");
    expect(component.groundTruthSettings.showGroundTruth).toEqual(false);
    expect(component.showClasses).toEqual([true, true]);
    expect(component.classColors).toEqual(["color1", "color2"]);
  });

  it('dataset subscription should set selectedDataset, reset image and show selection', () => {
    const selectedDatasetChangedService = TestBed.inject(SelectedDatasetChangedService);
    const dataset = {name: "test_dataset", classes: [], colors: []};

    selectedDatasetChangedService.publish(dataset)

    expect(component.selectedDataset).toEqual(dataset);
    expect(component.selectedImage).toEqual("");
    expect(component.groundTruthSettings.showGroundTruth).toEqual(false);
    expect(component.showClasses).toEqual([]);
    expect(component.classColors).toEqual([]);
  });

  it('image subscription should set selectedImage and trigger #selectionChanged', () => {
    const selectedImageChangedService = TestBed.inject(SelectedImageChangedService);
    const spy = spyOn(component, 'selectionChanged');

    selectedImageChangedService.publish("test_image.jpg")

    expect(component.selectedImage).toEqual("test_image.jpg");
    expect(spy).toHaveBeenCalled();
  });

  it('#selectionChanged should publish empty string if show gt not checked anymore', () => {
    const groundTruthChangedService = TestBed.inject(GroundTruthChangedService);
    const spy = spyOn(groundTruthChangedService, 'publish');

    component.selectionChanged();

    expect(spy).toHaveBeenCalledWith("");
  });

  it('#selectionChanged should trigger #getGroundTruth if dataset and image are selected', () => {
    const spy = spyOn(component, 'getGroundTruth');
    const dataset = {name: "test_dataset"}
    component.groundTruthSettings.showGroundTruth = true;
    component.selectedDataset = dataset;
    component.selectedImage = "test_image.jpg";

    component.selectionChanged();

    expect(spy).toHaveBeenCalled();
  });

  it('#selectionChanged should not trigger #getGroundTruth if dataset and image are not selected', () => {
    const spy = spyOn(component, 'getGroundTruth');
    component.selectedDataset = {name: ""};
    component.selectedImage = "";

    component.selectionChanged();

    expect(spy).not.toHaveBeenCalled();
  });

  it('#setClassColors should set classes in groundTruthSettings', () => {
    component.showClasses = [true, true]
    component.classColors = ["color1", "newColor"]
    component.selectedDataset = {name: "test_dataset", classes: ["class1", "class2"], colors: ["color1", "color2"]};

    component.setClassColors();

    expect(component.groundTruthSettings.classes).toEqual(["class1", "class2"]);
    expect(component.groundTruthSettings.colors).toEqual(["color1", "newColor"]);
  });

  it('#setClassColors should not set classes in groundTruthSettings if all classes are false', () => {
    component.showClasses = [false, false]
    component.classColors = ["color1", "newColor"]
    component.selectedDataset = {name: "test_dataset", classes: ["class1", "class2"], colors: ["color1", "color2"]};

    component.setClassColors();

    expect(component.groundTruthSettings.classes).toEqual([]);
    expect(component.groundTruthSettings.colors).toEqual([]);
  });

  it('#ngOnDestroy unsubscribes from all subscriptions', () => {
    const selectedImageChangedSpy = spyOn(component.selectedImageChanged, 'unsubscribe');
    const selectedDatasetChangedSpy = spyOn(component.selectedDatasetChanged, 'unsubscribe');

    component.ngOnDestroy();

    expect(selectedImageChangedSpy).toHaveBeenCalled();
    expect(selectedDatasetChangedSpy).toHaveBeenCalled();
  });
});
