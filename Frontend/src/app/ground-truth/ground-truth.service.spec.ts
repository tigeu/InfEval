import {TestBed} from '@angular/core/testing';

import {GroundTruthService} from './ground-truth.service';
import {HttpClientModule} from "@angular/common/http";

describe('GroundTruthService', () => {
  let service: GroundTruthService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
      ]
    });
    service = TestBed.inject(GroundTruthService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
