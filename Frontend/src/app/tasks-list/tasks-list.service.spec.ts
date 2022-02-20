import {TestBed} from '@angular/core/testing';

import {TasksListService} from './tasks-list.service';
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {of} from "rxjs";
import {TasksFile} from "./tasks-file";

describe('TasksListService', () => {
  let service: TasksListService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule
      ]
    });
    service = TestBed.inject(TasksListService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('#getTasksList should return array of TaskFiles', () => {
    const http = TestBed.inject(HttpClient);
    const taskFiles: TasksFile[] = [
      {name: "task1", description: "desc1", fileName: "file1", progress: 0, started: new Date(), finished: new Date()},
      {name: "task2", description: "desc2", fileName: "file2", progress: 50, started: new Date(), finished: new Date()},
      {name: "task3", description: "desc3", fileName: "file3", progress: 90, started: new Date(), finished: new Date()},
    ]

    spyOn(http, 'get').and.returnValue(of(taskFiles));

    service.getTasksList().subscribe(value => {
      expect(value).toBe(taskFiles);
    });
  });

  it('#getTasksList should return empty array if no models', () => {
    const http = TestBed.inject(HttpClient);
    const taskFiles: TasksFile[] = []

    spyOn(http, 'get').and.returnValue(of(taskFiles));

    service.getTasksList().subscribe(value => {
      expect(value).toBe(taskFiles);
    });
  });

  it('#getTasksList should return array with one element if only one model', () => {
    const http = TestBed.inject(HttpClient);
    const taskFiles: TasksFile[] = [
      {name: "task1", description: "desc1", fileName: "file1", progress: 0, started: new Date(), finished: new Date()},
    ]

    spyOn(http, 'get').and.returnValue(of(taskFiles));

    service.getTasksList().subscribe(value => {
      expect(value).toBe(taskFiles);
    });
  });
});
