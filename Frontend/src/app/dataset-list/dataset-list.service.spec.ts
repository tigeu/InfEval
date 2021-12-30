import {TestBed} from '@angular/core/testing';

import {DatasetListService} from './dataset-list.service';
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {FormsModule} from "@angular/forms";
import {UploadMainComponent} from "../upload-main/upload-main.component";
import {of} from "rxjs";
import {DatasetFile} from "./dataset-file";

describe('DatasetListService', () => {
  let service: DatasetListService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        FormsModule,
      ],
      declarations: [UploadMainComponent]
    });
    service = TestBed.inject(DatasetListService);
  });


  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('#getDatasetList should return array of DatasetFiles', () => {
    const http = TestBed.inject(HttpClient);
    const datasetFiles: DatasetFile[] = [
      {name: "test_dataset1"},
      {name: "test_dataset2"},
      {name: "test_dataset3"},
    ]

    const fakeDataset: DatasetFile = {name: "other_dataset"};
    spyOn(http, 'get').and.returnValue(of(datasetFiles));

    service.getDatasetList().subscribe(value => {
      expect(value).toBe(datasetFiles);
      expect(value).not.toContain(fakeDataset);
    });
  });

  it('#getDatasetList should return empty array if no datasets', () => {
    const http = TestBed.inject(HttpClient);
    const datasetFiles: DatasetFile[] = []

    spyOn(http, 'get').and.returnValue(of(datasetFiles));

    service.getDatasetList().subscribe(value => {
      expect(value).toBe(datasetFiles);
    });
  });

  it('#getDatasetList should return array with one element if only one dataset', () => {
    const http = TestBed.inject(HttpClient);
    const datasetFiles: DatasetFile[] = [
      {name: "test_dataset1"}
    ]

    spyOn(http, 'get').and.returnValue(of(datasetFiles));

    service.getDatasetList().subscribe(value => {
      expect(value).toBe(datasetFiles);
    });
  });
});
