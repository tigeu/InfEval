import {ComponentFixture, TestBed} from '@angular/core/testing';

import {MainComponent} from './main.component';
import {HttpClientModule} from "@angular/common/http";
import {ImageComponent} from "../image/image.component";
import {ImageFilesComponent} from "../image-files/image-files.component";
import {DatasetListComponent} from "../dataset-list/dataset-list.component";
import {ToolboxComponent} from "../toolbox/toolbox.component";
import {GroundTruthComponent} from "../ground-truth/ground-truth.component";
import {PredictionComponent} from "../prediction/prediction.component";

describe('MainComponent', () => {
  let component: MainComponent;
  let fixture: ComponentFixture<MainComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
      ],
      declarations: [
        MainComponent,
        ImageComponent,
        ImageFilesComponent,
        DatasetListComponent,
        ToolboxComponent,
        GroundTruthComponent,
        PredictionComponent
      ],
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MainComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
