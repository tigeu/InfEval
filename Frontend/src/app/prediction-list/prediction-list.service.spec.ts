import { TestBed } from '@angular/core/testing';

import { PredictionListService } from './prediction-list.service';

describe('PredictionListService', () => {
  let service: PredictionListService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PredictionListService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
