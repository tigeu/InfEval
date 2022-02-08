import {TestBed} from '@angular/core/testing';

import {ModelListService} from './model-list.service';
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {of} from "rxjs";
import {ModelFile} from "./model-file";

describe('ModelListService', () => {
  let service: ModelListService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule
      ]
    });
    service = TestBed.inject(ModelListService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('#getModelList should return array of ModelFiles', () => {
    const http = TestBed.inject(HttpClient);
    const modelFiles: ModelFile[] = [
      {name: "model1", type: "type1"},
      {name: "model2", type: "type1"},
      {name: "model3", type: "type2"},
    ]

    const fakeModel: ModelFile = {name: "other_model", type: "other_type"};
    spyOn(http, 'get').and.returnValue(of(modelFiles));

    service.getModelList().subscribe(value => {
      expect(value).toBe(modelFiles);
      expect(value).not.toContain(fakeModel);
    });
  });

  it('#getModelList should return empty array if no models', () => {
    const http = TestBed.inject(HttpClient);
    const modelFiles: ModelFile[] = []

    spyOn(http, 'get').and.returnValue(of(modelFiles));

    service.getModelList().subscribe(value => {
      expect(value).toBe(modelFiles);
    });
  });

  it('#getModelList should return array with one element if only one model', () => {
    const http = TestBed.inject(HttpClient);
    const modelFiles: ModelFile[] = [
      {name: "model1", type: "type1"}
    ]

    spyOn(http, 'get').and.returnValue(of(modelFiles));

    service.getModelList().subscribe(value => {
      expect(value).toBe(modelFiles);
    });
  });
});
