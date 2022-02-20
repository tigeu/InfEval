import {ComponentFixture, discardPeriodicTasks, fakeAsync, TestBed, tick} from '@angular/core/testing';

import {TasksListComponent} from './tasks-list.component';
import {HttpClientModule} from "@angular/common/http";
import {of} from "rxjs";
import {TasksFile} from "./tasks-file";
import {TasksListService} from "./tasks-list.service";

describe('TasksListComponent', () => {
  let component: TasksListComponent;
  let fixture: ComponentFixture<TasksListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientModule
      ],
      declarations: [
        TasksListComponent
      ]
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TasksListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('fetch taskslist in an interval of 5000ms', fakeAsync(() => {
    const spy = spyOn(component, 'getTasksList');
    component.ngOnInit();
    tick(5000);
    expect(spy).toHaveBeenCalledTimes(1);
    tick(5000);
    expect(spy).toHaveBeenCalledTimes(2);
    discardPeriodicTasks();
  }));

  it('#getTasksList should set datasetList', () => {
    const taskFiles: TasksFile[] = [
      {name: "task1", description: "desc1", fileName: "file1", progress: 0, started: new Date(), finished: new Date()},
      {name: "task2", description: "desc2", fileName: "file2", progress: 50, started: new Date(), finished: new Date()},
      {name: "task3", description: "desc3", fileName: "file3", progress: 90, started: new Date(), finished: new Date()},
    ]

    const tasksListService = TestBed.inject(TasksListService);
    spyOn(tasksListService, 'getTasksList').and.returnValue(of(taskFiles));

    component.getTasksList();

    expect(component.tasksList).toBe(taskFiles);
  });

  it('#ngOnDestroy unsubscribes from tasks subscription', () => {
    const tasksListSubscriptionSpy = spyOn(component.tasksListSubscription, 'unsubscribe');

    component.ngOnDestroy();

    expect(tasksListSubscriptionSpy).toHaveBeenCalled();
  });
});
