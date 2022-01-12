import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GroundTruthComponent } from './ground-truth.component';

describe('GroundTruthComponent', () => {
  let component: GroundTruthComponent;
  let fixture: ComponentFixture<GroundTruthComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GroundTruthComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GroundTruthComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
