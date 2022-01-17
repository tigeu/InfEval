import {ComponentFixture, TestBed} from '@angular/core/testing';

import {MainComponent} from './main.component';
import {Heartbeat} from "./heartbeat";
import {HeartbeatService} from "./heartbeat.service";
import {of} from "rxjs";
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

  it('should be initialized with heartbeat of 1', () => {
    const heartbeat: Heartbeat = {count: 1};

    expect(component.heartbeat).toEqual(heartbeat);
  })

  it('#getHeartbeat should increment heartbeat', () => {
    const incrementedHeartbeat: Heartbeat = {count: 2};
    const fakeHeartbeat: Heartbeat = {count: 3};
    const heartbeatService = TestBed.inject(HeartbeatService);
    spyOn(heartbeatService, 'getHeartbeat')
      .and.returnValue(of(incrementedHeartbeat));

    component.getHeartbeat();

    expect(component.heartbeat).toBe(incrementedHeartbeat);
    expect(component.heartbeat).not.toBe(fakeHeartbeat);
  });

  /*it('should render heartbeat', () => {
    expect(fixture.debugElement.query(By.css('#heartbeat')).nativeElement.innerText).toContain(1);
  });

  it('fetch heartbeat in an interval of 5000ms', fakeAsync(() => {
    const spy = spyOn(component, 'getHeartbeat');
    component.ngOnInit();
    tick(5000);
    expect(spy).toHaveBeenCalledTimes(1);
    tick(5000);
    expect(spy).toHaveBeenCalledTimes(2);
    discardPeriodicTasks();
  }));*/
});
