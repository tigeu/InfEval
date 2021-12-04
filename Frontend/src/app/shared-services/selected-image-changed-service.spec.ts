import {TestBed} from '@angular/core/testing';

import {SelectedImageChangedService} from './selected-image-changed-service';
import {HttpClientTestingModule} from "@angular/common/http/testing";
import {Image} from "../image/image";

describe('SelectedImageChangedService', () => {
  let service: SelectedImageChangedService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
      ],
      providers: []
    });
    service = TestBed.inject(SelectedImageChangedService);
  });

  it('should be created', () => {
    service = TestBed.inject(SelectedImageChangedService);

    expect(service).toBeTruthy();
  });

  it('#newData should return published image data', () => {
    const newImage: Image = {file: new File([""], "test_image.jpg")};
    const fakeImage: Image = {file: new File(["an"], "other_image.jpg")};

    // assert before act
    service.newData.subscribe((data: any) => {
      expect(data).toBe(newImage)
      expect(data).not.toBe(fakeImage)
    });

    service.publish(newImage);
  });
})
