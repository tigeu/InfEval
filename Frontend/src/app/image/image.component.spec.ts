import {ComponentFixture, TestBed} from '@angular/core/testing';

import {ImageComponent} from './image.component';
import {HttpClientModule} from "@angular/common/http";
import {SelectedImageChangedService} from "../shared-services/selected-image-changed-service";
import {of} from "rxjs";
import {Image} from "./image";
import {ImageService} from "./image.service";
import {By} from "@angular/platform-browser";

describe('ImageComponent', () => {
  let component: ImageComponent;
  let fixture: ComponentFixture<ImageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
      ],
      providers: [
        SelectedImageChangedService
      ],
      declarations: [ImageComponent]
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

    component.getImage("test_image.jpg");

    expect(component.image).toBe(newImage);
    expect(component.image).not.toBe(fakeImage)
  });

  it('#getImage should change imageUrl', () => {
    const newImage: Image = {file: new File([""], "test_image.jpg")};
    const imageService = TestBed.inject(ImageService);
    spyOn(imageService, 'getImage').withArgs("test_image.jpg").and.returnValue(of(newImage));

    component.getImage("test_image.jpg");

    expect(component.imageUrl).toBe('data:image/jpg;base64,' + newImage["file"]);
  });

  it('subscription should trigger #getimage', () => {
    const selectedImageChangedService = TestBed.inject(SelectedImageChangedService);
    const spy = spyOn(component, 'getImage');

    selectedImageChangedService.publish("test_image.jpg")
    expect(spy).toHaveBeenCalledWith("test_image.jpg");
  });

  it('should not render image if image is undefined or null', () => {
    expect(fixture.debugElement.query(By.css('#selected-image'))).toBeNull();
  });

  it('should render image if image given', () => {
    const newImage: Image = {file: new File([""], "test_image.jpg")};
    const imageService = TestBed.inject(ImageService);

    spyOn(imageService, 'getImage').withArgs("test_image.jpg").and.returnValue(of(newImage));

    component.getImage("test_image.jpg");

    expect(component.imageUrl).toBeTruthy();
    fixture.detectChanges();
    expect(fixture.debugElement.query(By.css('#selected-image')).nativeElement.src).toBeTruthy();
  });

  it('#resetImage should reset image', () => {
    component.resetImage();

    expect(component.image).toEqual({file: new File([""], "")});
    expect(component.imageUrl).toBe("");
  })
});
