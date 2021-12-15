import {TestBed} from '@angular/core/testing';

import {HttpClient} from "@angular/common/http";

import {HttpClientTestingModule} from "@angular/common/http/testing";
import {of} from "rxjs";
import {RegisterService} from "./register.service";

describe('RegisterService', () => {
  let service: RegisterService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
      ],
      providers: []
    });
    service = TestBed.inject(RegisterService);
  });

  it('should be created', () => {
    service = TestBed.inject(RegisterService);

    expect(service).toBeTruthy();
  });

  it('#register should return registered username and email', () => {
    const http = TestBed.inject(HttpClient);
    const user = {
      "username": "test",
      "email": "test@test.test"
    }

    spyOn(http, 'post').and.returnValue(of(user));

    service.register("test", "test@test.test", "test").subscribe(value => {
      expect(value).toBe(user);
    });
  });
})
