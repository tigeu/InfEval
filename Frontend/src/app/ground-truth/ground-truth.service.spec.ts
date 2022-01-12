import { TestBed } from '@angular/core/testing';

import { GroundTruthService } from './ground-truth.service';

describe('GroundTruthService', () => {
  let service: GroundTruthService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GroundTruthService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
