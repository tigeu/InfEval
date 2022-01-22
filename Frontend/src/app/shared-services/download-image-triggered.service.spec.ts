import {TestBed} from '@angular/core/testing';

import {DownloadImageTriggeredService} from './download-image-triggered.service';

describe('DownloadImageTriggeredService', () => {
  let service: DownloadImageTriggeredService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DownloadImageTriggeredService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('#newData should return true', () => {
    // assert before act
    service.newData.subscribe((data: any) => {
      expect(data).toBe(true)
    });

    service.publish(true);
  });

  it('#newData should return false', () => {
    // assert before act
    service.newData.subscribe((data: any) => {
      expect(data).toBe(false)
    });

    service.publish(false);
  });
});
