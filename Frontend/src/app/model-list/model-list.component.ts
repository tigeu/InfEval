import {Component, OnInit} from '@angular/core';
import {ModelFile} from "./model-file";
import {ModelListService} from "./model-list.service";
import {SelectedModelChangedService} from "../shared-services/selected-model-changed.service";

@Component({
  selector: 'app-model-list',
  templateUrl: './model-list.component.html',
  styleUrls: ['./model-list.component.css']
})
export class ModelListComponent implements OnInit {
  /*
  Component that gets a list of models from /model-list and displays them in a dropdown menu. Selected model is
  sent to SelectedModelChangedService.

  Attributes
  ----------
  modelListService : ModelListService
    Service for retrieving a list of models
  modelChangedService : SelectedModelChangedService
    Service for publishing the selected model
  modelList : ModelFile[]
    List of retrieved models

  Methods
  -------
  getModelList()
    Calls service to retrieve the model list and save it to modelList
  selectedModelChanged(model: string)
    Finds the selected model and publishes it using a shared service
  */
  modelList: ModelFile[] = [];

  constructor(private modelListService: ModelListService,
              private modelChangedService: SelectedModelChangedService) {
    /*
    Retrieve list of models

    Parameters
    ----------
    modelListService : ModelListService
      Service for retrieving a list of models
    modelChangedService : SelectedModelChangedService
      Service for publishing the selected model
    */
    this.getModelList()
  }

  ngOnInit(): void {
  }

  getModelList(): void {
    /*
    Calls service to retrieve the model list and save it to modelList
    */
    this.modelListService.getModelList()
      .subscribe((modelList: ModelFile[]) => {
        this.modelList = modelList
      })
  }

  selectedModelChanged(model: string) {
    /*
    Finds the selected model and publishes it using a shared service

    Parameters
    ----------
    model : string
      Name of selected model
    */
    const selectedModel = this.modelList.find(x => x.name == model)
    if (selectedModel)
      this.modelChangedService.publish(selectedModel);
  }
}
