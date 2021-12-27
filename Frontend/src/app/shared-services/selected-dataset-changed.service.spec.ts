import {TestBed} from '@angular/core/testing';

import {SelectedDatasetChangedService} from './selected-dataset-changed.service';

describe('SelectedDatasetChangedService', () => {
  let service: SelectedDatasetChangedService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SelectedDatasetChangedService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
