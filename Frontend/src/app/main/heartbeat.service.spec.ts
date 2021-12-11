import {TestBed} from '@angular/core/testing';

import {HeartbeatService} from './heartbeat.service';
import {HttpClient} from "@angular/common/http";
import {Heartbeat} from "./heartbeat";
import {HttpClientTestingModule} from "@angular/common/http/testing";
import {of} from "rxjs";

describe('HeartbeatService', () => {
  let service: HeartbeatService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
      ],
      providers: []
    });
    service = TestBed.inject(HeartbeatService);
  });

  it('should be created', () => {
    service = TestBed.inject(HeartbeatService);

    expect(service).toBeTruthy();
  });

  it('#getHeartbeat should return incremented heartbeat number', () => {
    const http = TestBed.inject(HttpClient);
    const heartbeat: Heartbeat = {count: 0};
    const response: Heartbeat = {count: 1};
    const fakeHeartbeat: Heartbeat = {count: 2};
    const httpGetSpy: jasmine.Spy<any> = spyOn(http, 'get').and.returnValue(of(response));

    service.getHeartbeat(heartbeat).subscribe(value => {
      expect(value).toBe(response);
      expect(value).not.toBe(fakeHeartbeat);
    });
  });
})
