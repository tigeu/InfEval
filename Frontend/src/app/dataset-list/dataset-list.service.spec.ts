import {TestBed} from '@angular/core/testing';

import {DatasetListService} from './dataset-list.service';
import {HttpClientModule} from "@angular/common/http";
import {FormsModule} from "@angular/forms";
import {UploadMainComponent} from "../upload-main/upload-main.component";

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
});
