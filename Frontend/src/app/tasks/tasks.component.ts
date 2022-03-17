import {Component, OnInit} from '@angular/core';
import {Subscription} from "rxjs";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";
import {SelectedModelChangedService} from "../shared-services/selected-model-changed.service";
import {DatasetFile} from "../dataset-list/dataset-file";
import {ModelFile} from "../model-list/model-file";
import {TasksService} from "./tasks.service";
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {HttpErrorResponse} from "@angular/common/http";

@Component({
  selector: 'app-tasks',
  templateUrl: './tasks.component.html',
  styleUrls: ['./tasks.component.css']
})
export class TasksComponent implements OnInit {
  /*
  Component that starts an inference task based on the entries in form.

  Attributes
  ----------
  tasksService : TasksService
    Service for starting task
  formBuilder : FormBuilder
    FormBuilder for task form
  selectedDatasetChangedService : SelectedDatasetChangedService
    Service for retrieving the selected dataset from a shared service
  selectedModelChangedService : SelectedModelChangedService
    Service for retrieving the selected model from a shared service
  dataset : DatasetFile
    Currently selected dataset
  model : ModelFile
    Currently selected model
  selectedDatasetChanged : Subscription
    Subscription for retrieving the selected dataset from a shared service
  selectedModelChanged : Subscription
    Subscription for retrieving the selected model from a shared service
  tasksForm : FormGroup
    FormGroup for task form
  successMessage : string
    Message shown when task is successfully finished
  errorMessage : string
    Message shown when there was an error
  taskNameErrorMessage : string
    Error message for task name
  taskDescriptionErrorMessage : string
    Error message for task description
  fileNameErrorMessage : string
    Error message for file name
  datasetErrorMessage : string
    Error message for dataset
  modelErrorMessage : string
    Error message for model

  Methods
  -------
  startTask(taskName: string, taskDescription: string, fileName: string, dataset: string, model: string)
    Calls service to start task based on entered parameters
  onStartTask()
    Validates form and starts task
  validateForm(taskName: string, taskDescription: string, fileName: string, datasetName: string, modelName: string)
    Call validation methods for all form fields
  validateTaskName(taskName: string)
    Validate task name (not empty, alphanumeric)
  validateTaskDescription(taskDescription: string)
    Validate task description (not empty, alphanumeric)
  validateFileName(fileName: string)
    Validate file name (not empty, alphanumeric)
  validateDataset(datasetName: string)
    Validate dataset name (not empty)
  validateModel(modelName: string)
    Validate model name (not empty)
  setErrorMessage(res: HttpErrorResponse)
    Set error messaged from Error Response
  setSuccessMessage()
    Set success message
  */
  dataset: DatasetFile = {name: ''};
  model: ModelFile = {name: '', type: ''};

  selectedDatasetChanged: Subscription;
  selectedModelChanged: Subscription;

  tasksForm: FormGroup;
  successMessage: string = "";
  errorMessage: string = "";
  taskNameErrorMessage: string = "";
  taskDescriptionErrorMessage: string = "";
  fileNameErrorMessage: string = "";
  datasetErrorMessage: string = "";
  modelErrorMessage: string = "";

  constructor(private tasksService: TasksService,
              private formBuilder: FormBuilder,
              private selectedDatasetChangedService: SelectedDatasetChangedService,
              private selectedModelChangedService: SelectedModelChangedService) {
    /*
    Initialise subscriptions for retrieving selected dataset and selected model

    Parameters
    ----------
    tasksService : TasksService
      Service for starting task
    formBuilder : FormBuilder
      FormBuilder for task form
    selectedDatasetChangedService : SelectedDatasetChangedService
      Service for retrieving the selected dataset from a shared service
    selectedModelChangedService : SelectedModelChangedService
      Service for retrieving the selected model from a shared service
    */
    this.tasksForm = this.formBuilder.group({
      taskName: ['', Validators.required],
      taskDescription: [''],
      fileName: ['', Validators.required]
    });
    this.selectedDatasetChanged = this.selectedDatasetChangedService.newData.subscribe((data: DatasetFile) => {
      this.dataset = data;
    })
    this.selectedModelChanged = this.selectedModelChangedService.newData.subscribe((data: ModelFile) => {
      this.model = data;
    })
  }

  ngOnInit(): void {
  }

  ngOnDestroy(): void {
    /*
    Unsubscribe from all subscriptions
    */
    this.selectedDatasetChanged.unsubscribe();
    this.selectedModelChanged.unsubscribe();
  }

  startTask(taskName: string, taskDescription: string, fileName: string, dataset: string, model: string) {
    /*
    Calls service to start task based on entered parameters

    Parameters
    ----------
    taskName : string
      Entered task name
    taskDescription : string
      Entered task description
    fileName : string
      Entered file name
    dataset : string
      Selected dataset
    model : string
      Selected model
    */
    this.tasksService.startTask(taskName, taskDescription, fileName, dataset, model)
      .subscribe({
        next: this.setSuccessMessage.bind(this),
        error: this.setErrorMessage.bind(this)
      })
  }

  onStartTask() {
    /*
    Validates form and starts task
    */
    this.errorMessage = "";
    const value = this.tasksForm.value;
    const formValid = this.validateForm(value.taskName, value.taskDescription, value.fileName, this.dataset.name, this.model.name);
    if (formValid)
      this.startTask(value.taskName, value.taskDescription, value.fileName, this.dataset.name, this.model.name);
  }

  validateForm(taskName: string, taskDescription: string, fileName: string, datasetName: string, modelName: string): boolean {
    /*
    Call validation methods for all form fields

    Parameters
    ----------
    taskName : string
      Entered task name
    taskDescription : string
      Entered task description
    fileName : string
      Entered file name
    datasetName : string
      Selected dataset
    modelName : string
      Selected model
    */
    const taskNameValid = this.validateTaskName(taskName);
    const taskDescriptionValid = this.validateTaskDescription(taskDescription);
    const fileNameValid = this.validateFileName(fileName);
    const datasetNameValid = this.validateDataset(datasetName);
    const modelNameValid = this.validateModel(modelName);
    return taskNameValid && taskDescriptionValid && fileNameValid && datasetNameValid && modelNameValid;
  }

  validateTaskName(taskName: string): boolean {
    /*
    Validate task name (not empty, alphanumeric)

    Parameters
    ----------
    taskName : string
      Entered task name
    */
    const taskNameRegExp = new RegExp(/^[a-z0-9]+$/i);
    if (!taskName) {
      this.taskNameErrorMessage = "Task name missing";
      return false;
    }
    if (taskName && !taskNameRegExp.test(taskName)) {
      this.taskNameErrorMessage = "Task name is not alphanumeric";
      return false;
    }
    this.taskNameErrorMessage = "";
    return true;
  }

  validateTaskDescription(taskDescription: string): boolean {
    /*
    Validate task description (not empty, alphanumeric)

    Parameters
    ----------
    taskDescription : string
      Entered task description
    */
    const taskDescriptionRegExp = new RegExp(/^[a-z0-9 ]+$/i);
    if (taskDescription && !taskDescriptionRegExp.test(taskDescription)) {
      this.taskDescriptionErrorMessage = "Description is not alphanumeric";
      return false;
    }
    this.taskDescriptionErrorMessage = "";
    return true;
  }

  validateFileName(fileName: string): boolean {
    /*
    Validate file name (not empty, alphanumeric)

    Parameters
    ----------
    fileName : string
      Entered file name
    */
    const fileNameRegExp = new RegExp(/^[a-z0-9]+$/i);
    if (!fileName) {
      this.fileNameErrorMessage = "File name missing";
      return false;
    }
    if (fileName && !fileNameRegExp.test(fileName)) {
      this.fileNameErrorMessage = "File name is not alphanumeric";
      return false;
    }
    this.fileNameErrorMessage = "";
    return true;
  }

  validateDataset(datasetName: string): boolean {
    /*
    Validate dataset (not empty)

    Parameters
    ----------
    datasetName : string
      Selected dataset name
    */
    if (!datasetName) {
      this.datasetErrorMessage = "No dataset selected";
      return false;
    }
    this.datasetErrorMessage = "";
    return true;
  }

  validateModel(modelName: string): boolean {
    /*
    Validate model (not empty)

    Parameters
    ----------
    modelName : string
      Selected model name
    */
    if (!modelName) {
      this.modelErrorMessage = "No model selected";
      return false;
    }
    this.modelErrorMessage = "";
    return true;
  }

  setErrorMessage(res: HttpErrorResponse) {
    /*
    Set error messaged from Error Response
    */
    this.errorMessage = res.error;
  }

  setSuccessMessage() {
    /*
    Set success message
    */
    this.successMessage = "Task successfully started";
  }
}
