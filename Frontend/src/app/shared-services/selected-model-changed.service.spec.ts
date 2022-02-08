import {TestBed} from '@angular/core/testing';

import {SelectedModelChangedService} from './selected-model-changed.service';

describe('SelectedModelChangedService', () => {
  let service: SelectedModelChangedService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SelectedModelChangedService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
