import { TestBed } from '@angular/core/testing';

import { SelectedPredictionChangedService } from './selected-prediction-changed.service';

describe('SelectedPredictionChangedService', () => {
  let service: SelectedPredictionChangedService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SelectedPredictionChangedService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
