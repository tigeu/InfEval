import {TestBed} from '@angular/core/testing';

import {TasksService} from './tasks.service';
import {HttpClient, HttpClientModule, HttpResponse} from "@angular/common/http";
import {of} from "rxjs";

describe('TasksService', () => {
  let service: TasksService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
      ],
    });
    service = TestBed.inject(TasksService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('#startTask should return request', () => {
    const http = TestBed.inject(HttpClient);
    const response = new HttpResponse({status: 200})

    spyOn(http, 'post').and.returnValue(of(response));

    service.startTask("task_name", "desc", "file", "dataset", "model")
      .subscribe(res => {
        expect(res).toBe(response);
      });
  });
});
