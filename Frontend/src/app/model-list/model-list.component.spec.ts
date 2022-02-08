import {ComponentFixture, TestBed} from '@angular/core/testing';

import {ModelListComponent} from './model-list.component';
import {HttpClientModule} from "@angular/common/http";
import {of} from "rxjs";
import {ModelFile} from "./model-file";
import {ModelListService} from "./model-list.service";
import {SelectedModelChangedService} from "../shared-services/selected-model-changed.service";

describe('ModelListComponent', () => {
  let component: ModelListComponent;
  let fixture: ComponentFixture<ModelListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [
        ModelListComponent
      ],
      imports: [
        HttpClientModule
      ]
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ModelListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#getModelList should set modelList', () => {
    const modelFiles: ModelFile[] = [
      {name: "model1", type: "type1"},
      {name: "model2", type: "type1"},
      {name: "model3", type: "type2"},
    ]

    const modelListService = TestBed.inject(ModelListService);
    spyOn(modelListService, 'getModelList').and.returnValue(of(modelFiles));

    component.getModelList();

    expect(component.modelList).toBe(modelFiles);
  });

  it('#getModelList should create set modelList to empty array if no models exist', () => {
    const modelFiles: ModelFile[] = []
    const modelListService = TestBed.inject(ModelListService);
    spyOn(modelListService, 'getModelList').and.returnValue(of(modelFiles));

    component.getModelList();

    expect(component.modelList).toBe(modelFiles);
  });

  it('click should publish new selected model', () => {
    const selectedModelChangedService = TestBed.inject(SelectedModelChangedService);
    const models = [{'name': "model1", "type": "type1"}, {'name': "model2", "type": "type2"}]
    spyOn(selectedModelChangedService, 'publish').withArgs({'name': "model1", "type": "type1"});
    component.modelList = models;

    component.selectedModelChanged("model1");

    expect(selectedModelChangedService.publish).toHaveBeenCalledWith({'name': "model1", "type": "type1"})
  });
});
