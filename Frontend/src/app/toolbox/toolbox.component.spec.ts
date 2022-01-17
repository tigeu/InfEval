import {ComponentFixture, TestBed} from '@angular/core/testing';

import {ToolboxComponent} from './toolbox.component';
import {GroundTruthComponent} from "../ground-truth/ground-truth.component";
import {HttpClientModule} from "@angular/common/http";
import {PredictionComponent} from "../prediction/prediction.component";

describe('ToolboxComponent', () => {
  let component: ToolboxComponent;
  let fixture: ComponentFixture<ToolboxComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [
        ToolboxComponent,
        GroundTruthComponent,
        PredictionComponent
      ],
      imports: [
        HttpClientModule
      ]

    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ToolboxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
