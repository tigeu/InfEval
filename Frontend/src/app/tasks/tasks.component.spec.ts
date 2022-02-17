import {ComponentFixture, TestBed} from '@angular/core/testing';

import {TasksComponent} from './tasks.component';
import {HttpClientModule, HttpErrorResponse, HttpResponse} from "@angular/common/http";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {DatasetListComponent} from "../dataset-list/dataset-list.component";
import {ModelListComponent} from "../model-list/model-list.component";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";
import {SelectedModelChangedService} from "../shared-services/selected-model-changed.service";
import {of, throwError} from "rxjs";
import {TasksService} from "./tasks.service";

describe('TasksComponent', () => {
  let component: TasksComponent;
  let fixture: ComponentFixture<TasksComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        FormsModule,
        ReactiveFormsModule
      ],
      declarations: [
        TasksComponent,
        DatasetListComponent,
        ModelListComponent
      ]
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TasksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('dataset subscription should set dataset', () => {
    const selectedDatasetChangedService = TestBed.inject(SelectedDatasetChangedService);
    const dataset = {name: "test_dataset"};

    selectedDatasetChangedService.publish(dataset)

    expect(component.dataset).toEqual(dataset);
  });

  it('model subscription should set model', () => {
    const selectedModelChangedService = TestBed.inject(SelectedModelChangedService);
    const model = {name: "test_model", type: "tf2"};

    selectedModelChangedService.publish(model)

    expect(component.model).toEqual(model);
  });

  it('#startTask should trigger service call and set success message', () => {
    const tasksService = TestBed.inject(TasksService);
    const response = new HttpResponse({status: 200})

    const spy = spyOn(tasksService, 'startTask').and.returnValue(of(response));
    const messageSpy = spyOn(component, "setSuccessMessage");

    component.startTask("task", "desc", "file", "dataset", "model")

    expect(spy).toHaveBeenCalledWith("task", "desc", "file", "dataset", "model");
    expect(messageSpy).toHaveBeenCalled();
  });

  it('#startTask should trigger service call and set error message', () => {
    const tasksService = TestBed.inject(TasksService);

    const spy = spyOn(tasksService, 'startTask').and.returnValue(throwError(() => "error"));
    const messageSpy = spyOn(component, "setErrorMessage");

    component.startTask("task", "desc", "file", "dataset", "model")

    expect(spy).toHaveBeenCalledWith("task", "desc", "file", "dataset", "model");
    expect(messageSpy).toHaveBeenCalled();
  });

  it('#onStartTask should reset error message, validate form and start task', () => {
    const spy = spyOn(component, 'startTask');
    const validationSpy = spyOn(component, "validateForm").and.returnValue(true);

    component.tasksForm.value.taskName = "task";
    component.tasksForm.value.taskDescription = "desc";
    component.tasksForm.value.fileName = "file";
    component.dataset = {name: "dataset"};
    component.model = {name: "model", type: "tf2"};

    component.onStartTask()

    expect(validationSpy).toHaveBeenCalledWith("task", "desc", "file", "dataset", "model");
    expect(spy).toHaveBeenCalledWith("task", "desc", "file", "dataset", "model");
  });

  it('#onStartTask should not start task if validation fails', () => {
    const spy = spyOn(component, 'startTask');
    const validationSpy = spyOn(component, "validateForm").and.returnValue(false);

    component.onStartTask()

    expect(validationSpy).toHaveBeenCalled();
    expect(spy).not.toHaveBeenCalled();
  });

  it('#validateForm should call validation methods of all form items and return true if all are true', () => {
    const taskSpy = spyOn(component, 'validateTaskName').and.returnValue(true);
    const descriptionSpy = spyOn(component, 'validateTaskDescription').and.returnValue(true);
    const fileSpy = spyOn(component, 'validateFileName').and.returnValue(true);
    const datasetSpy = spyOn(component, 'validateDataset').and.returnValue(true);
    const modelSpy = spyOn(component, 'validateModel').and.returnValue(true);

    const result = component.validateForm("task", "desc", "file", "dataset", "model");

    expect(taskSpy).toHaveBeenCalledWith("task");
    expect(descriptionSpy).toHaveBeenCalledWith("desc");
    expect(fileSpy).toHaveBeenCalledWith("file");
    expect(datasetSpy).toHaveBeenCalledWith("dataset");
    expect(modelSpy).toHaveBeenCalledWith("model");
    expect(result).toBeTruthy();
  });

  it('#validateTaskName should return false if empty and set error', () => {
    const result = component.validateTaskName("");
    expect(result).not.toBeTruthy();
    expect(component.taskNameErrorMessage).toEqual("Task name missing");
  });

  it('#validateTaskName should return false if not alphanumeric and set error', () => {
    const result = component.validateTaskName("<<>><>");
    expect(result).not.toBeTruthy();
    expect(component.taskNameErrorMessage).toEqual("Task name is not alphanumeric");
  });

  it('#validateTaskName should return true and reset error', () => {
    const result = component.validateTaskName("validName");
    expect(result).toBeTruthy();
    expect(component.taskNameErrorMessage).toEqual("");
  });

  it('#validateTaskDescription should return false if not alphanumeric and set error', () => {
    const result = component.validateTaskDescription("<<>><>");
    expect(result).not.toBeTruthy();
    expect(component.taskDescriptionErrorMessage).toEqual("Description is not alphanumeric");
  });

  it('#validateTaskDescription should return true and reset error', () => {
    const result = component.validateTaskDescription("validName");
    expect(result).toBeTruthy();
    expect(component.taskDescriptionErrorMessage).toEqual("");
  });

  it('#validateFileName should return false if empty and set error', () => {
    const result = component.validateFileName("");
    expect(result).not.toBeTruthy();
    expect(component.fileNameErrorMessage).toEqual("File name missing");
  });

  it('#validateFileName should return false if not alphanumeric and set error', () => {
    const result = component.validateFileName("<<>><>");
    expect(result).not.toBeTruthy();
    expect(component.fileNameErrorMessage).toEqual("File name is not alphanumeric");
  });

  it('#validateFileName should return true and reset error', () => {
    const result = component.validateFileName("validName");
    expect(result).toBeTruthy();
    expect(component.fileNameErrorMessage).toEqual("");
  });

  it('#validateDataset should return false if no dataset selected', () => {
    const result = component.validateDataset("");
    expect(result).not.toBeTruthy();
    expect(component.datasetErrorMessage).toEqual("No dataset selected");
  });

  it('#validateDataset should return true and reset error', () => {
    const result = component.validateDataset("validName");
    expect(result).toBeTruthy();
    expect(component.datasetErrorMessage).toEqual("");
  });

  it('#validateModel should return false if no dataset selected', () => {
    const result = component.validateModel("");
    expect(result).not.toBeTruthy();
    expect(component.modelErrorMessage).toEqual("No model selected");
  });

  it('#validateModel should return true and reset error', () => {
    const result = component.validateModel("validName");
    expect(result).toBeTruthy();
    expect(component.modelErrorMessage).toEqual("");
  });

  it('#ngOnDestroy unsubscribes from all subscriptions', () => {
    const selectedDatasetChangedSpy = spyOn(component.selectedDatasetChanged, 'unsubscribe');
    const selectedModelChangedSpy = spyOn(component.selectedModelChanged, 'unsubscribe');

    component.ngOnDestroy();

    expect(selectedDatasetChangedSpy).toHaveBeenCalled();
    expect(selectedModelChangedSpy).toHaveBeenCalled();
  });

  it('#setErrorMessage should set error message', () => {
    const httpErrorResponse = new HttpErrorResponse({
      error: "error",
      status: 400,
      statusText: 'Bad Request'
    })

    component.setErrorMessage(httpErrorResponse);

    expect(component.errorMessage).toEqual("error");
  });

  it('#setSuccessMessage should set error message', () => {
    component.setSuccessMessage();

    expect(component.successMessage).toEqual("Task successfully started");
  });
});
