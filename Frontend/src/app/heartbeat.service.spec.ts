import {TestBed} from '@angular/core/testing';

import {HeartbeatService} from './heartbeat.service';
import {HttpClientModule} from "@angular/common/http";

describe('HeartbeatService', () => {
  let service: HeartbeatService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule
      ]
    });
    service = TestBed.inject(HeartbeatService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
