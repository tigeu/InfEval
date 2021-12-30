import {ComponentFixture, discardPeriodicTasks, fakeAsync, TestBed, tick} from '@angular/core/testing';

import {DatasetListComponent} from './dataset-list.component';
import {HttpClientModule} from "@angular/common/http";
import {FormsModule} from "@angular/forms";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatSelectModule} from "@angular/material/select";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
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
        BrowserAnimationsModule,
        MatFormFieldModule,
        MatSelectModule
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
    spyOn(selectedDatasetChangedService, 'publish').withArgs("test_dataset1");

    component.selectedDatasetChanged("test_dataset1");

    expect(selectedDatasetChangedService.publish).toHaveBeenCalledWith("test_dataset1")
  });

  it('fetch dataset-list in an interval of 10000ms', fakeAsync(() => {
    const spy = spyOn(component, 'getDatasetList');
    component.ngOnInit();
    tick(5000);
    expect(spy).toHaveBeenCalledTimes(1);
    tick(5000);
    expect(spy).toHaveBeenCalledTimes(2);
    discardPeriodicTasks();
  }));
});
