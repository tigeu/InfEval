import {ComponentFixture, TestBed} from '@angular/core/testing';

import {DatasetListComponent} from './dataset-list.component';
import {HttpClientModule} from "@angular/common/http";
import {FormsModule} from "@angular/forms";
import {SelectedDatasetChangedService} from "../shared-services/selected-dataset-changed.service";
import {of} from "rxjs";
import {DatasetFile} from "./dataset-file";
import {DatasetListService} from "./dataset-list.service";

describe('DatasetListComponent', () => {
  let component: DatasetListComponent;
  let fixture: ComponentFixture<DatasetListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        FormsModule,
      ],
      declarations: [DatasetListComponent]
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DatasetListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#getDatasetList should set datasetList', () => {
    const datasetFiles: DatasetFile[] = [
      {name: "test_dataset1"},
      {name: "test_dataset2"},
      {name: "test_dataset3"},
    ]

    const datasetListService = TestBed.inject(DatasetListService);
    spyOn(datasetListService, 'getDatasetList').and.returnValue(of(datasetFiles));

    component.getDatasetList();

    expect(component.datasetList).toBe(datasetFiles);
  });

  it('#getDatasetList should create set datasetList to empty array if no datasets exist', () => {
    const datasetFiles: DatasetFile[] = []
    const datasetListService = TestBed.inject(DatasetListService);
    spyOn(datasetListService, 'getDatasetList').and.returnValue(of(datasetFiles));

    component.getDatasetList();

    expect(component.datasetList).toBe(datasetFiles);
  });

  it('click should publish new selected dataset', () => {
    const selectedDatasetChangedService = TestBed.inject(SelectedDatasetChangedService);
    const datasets = [{'name': "test_dataset1"}, {'name': "test_dataset2"}]
    spyOn(selectedDatasetChangedService, 'publish').withArgs({'name': "test_dataset1"});
    component.datasetList = datasets;

    component.selectedDatasetChanged("test_dataset1");

    expect(selectedDatasetChangedService.publish).toHaveBeenCalledWith({'name': "test_dataset1"})
  });
});
