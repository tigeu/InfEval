import {TestBed} from '@angular/core/testing';

import {SelectedPredictionChangedService} from './selected-prediction-changed.service';

describe('SelectedPredictionChangedService', () => {
  let service: SelectedPredictionChangedService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SelectedPredictionChangedService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('#newData should return selected dataset', () => {
    const newDataset: string = "test_dataset1";
    const fakeDataset: string = "other_dataset";

    // assert before act
    service.newData.subscribe((data: any) => {
      expect(data).toBe(newDataset)
      expect(data).not.toBe(fakeDataset)
    });

    service.publish(newDataset);
  });
});
