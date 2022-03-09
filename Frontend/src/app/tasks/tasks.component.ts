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
    this.selectedDatasetChanged.unsubscribe();
    this.selectedModelChanged.unsubscribe();
  }

  startTask(taskName: string, taskDescription: string, fileName: string, dataset: string, model: string) {
    this.tasksService.startTask(taskName, taskDescription, fileName, dataset, model)
      .subscribe({
        next: this.setSuccessMessage.bind(this),
        error: this.setErrorMessage.bind(this)
      })
  }

  onStartTask() {
    this.errorMessage = "";
    const value = this.tasksForm.value;
    const formValid = this.validateForm(value.taskName, value.taskDescription, value.fileName, this.dataset.name, this.model.name);
    if (formValid)
      this.startTask(value.taskName, value.taskDescription, value.fileName, this.dataset.name, this.model.name);
  }

  validateForm(taskName: string, taskDescription: string, fileName: string, datasetName: string, modelName: string): boolean {
    const taskNameValid = this.validateTaskName(taskName);
    const taskDescriptionValid = this.validateTaskDescription(taskDescription);
    const fileNameValid = this.validateFileName(fileName);
    const datasetNameValid = this.validateDataset(datasetName);
    const modelNameValid = this.validateModel(modelName);
    return taskNameValid && taskDescriptionValid && fileNameValid && datasetNameValid && modelNameValid;
  }

  validateTaskName(taskName: string): boolean {
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
    const taskDescriptionRegExp = new RegExp(/^[a-z0-9 ]+$/i);
    if (taskDescription && !taskDescriptionRegExp.test(taskDescription)) {
      this.taskDescriptionErrorMessage = "Description is not alphanumeric";
      return false;
    }
    this.taskDescriptionErrorMessage = "";
    return true;
  }

  validateFileName(fileName: string): boolean {
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
    if (!datasetName) {
      this.datasetErrorMessage = "No dataset selected";
      return false;
    }
    this.datasetErrorMessage = "";
    return true;
  }

  validateModel(modelName: string): boolean {
    if (!modelName) {
      this.modelErrorMessage = "No model selected";
      return false;
    }
    this.modelErrorMessage = "";
    return true;
  }

  setErrorMessage(res: HttpErrorResponse) {
    this.errorMessage = res.error;
  }

  setSuccessMessage() {
    this.successMessage = "Task successfully started";
  }
}
