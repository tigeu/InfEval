import { TestBed } from '@angular/core/testing';

import { DatasetListService } from './dataset-list.service';

describe('DatasetListService', () => {
  let service: DatasetListService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DatasetListService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
