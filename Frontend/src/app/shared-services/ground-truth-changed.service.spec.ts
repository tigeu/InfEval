import {TestBed} from '@angular/core/testing';

import {GroundTruthChangedService} from './ground-truth-changed.service';
import {Image} from "../image/image";

describe('GroundTruthChangedService', () => {
  let service: GroundTruthChangedService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GroundTruthChangedService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('#newData should return published ground truth data', () => {
    const newGroundTruth: Image = {file: new File([""], "test_image.jpg")};

    // assert before act
    service.newData.subscribe((data: any) => {
      expect(data).toBe(newGroundTruth)
    });

    service.publish(newGroundTruth);
  });
});
