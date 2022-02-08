import {Component, OnInit} from '@angular/core';
import {Subscription} from "rxjs";
import {ModelFile} from "./model-file";
import {ModelListService} from "./model-list.service";
import {SelectedModelChangedService} from "../shared-services/selected-model-changed.service";

@Component({
  selector: 'app-model-list',
  templateUrl: './model-list.component.html',
  styleUrls: ['./model-list.component.css']
})
export class ModelListComponent implements OnInit {
  modelList: ModelFile[] = [];
  private modelListSubscription: Subscription = new Subscription;

  constructor(private modelListService: ModelListService,
              private modelChangedService: SelectedModelChangedService) {
  }

  ngOnInit(): void {
    this.getModelList()
  }

  ngOnDestroy(): void {
    this.modelListSubscription.unsubscribe();
  }

  getModelList(): void {
    this.modelListService.getModelList()
      .subscribe((modelList: ModelFile[]) => {
        this.modelList = modelList
      })
  }

  selectedModelChanged(model: string) {
    const selectedModel = this.modelList.find(x => x.name == model)
    if (selectedModel)
      this.modelChangedService.publish(selectedModel);
  }
}
