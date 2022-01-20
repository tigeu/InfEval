import {TestBed} from '@angular/core/testing';

import {SelectedPredictionChangedService} from './selected-prediction-changed.service';
import {DatasetFile} from "../dataset-list/dataset-file";

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
    const newDataset: DatasetFile = {name: "test_dataset1"};
    const fakeDataset: DatasetFile = {name: "other_dataset"};

    // assert before act
    service.newData.subscribe((data: any) => {
      expect(data).toBe(newDataset)
      expect(data).not.toBe(fakeDataset)
    });

    service.publish(newDataset);
  });
});
