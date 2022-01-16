import { TestBed } from '@angular/core/testing';

import { PredictionChangedService } from './prediction-changed.service';

describe('PredictionChangedService', () => {
  let service: PredictionChangedService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PredictionChangedService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
