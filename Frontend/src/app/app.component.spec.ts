import {ComponentFixture, discardPeriodicTasks, fakeAsync, TestBed, tick} from '@angular/core/testing';
import {RouterTestingModule} from '@angular/router/testing';
import {AppComponent} from './app.component';
import {HttpClientModule} from "@angular/common/http";
import {ImageComponent} from "./image/image.component";
import {ImageFilesComponent} from "./image-files/image-files.component";
import {SelectedImageChangedService} from "./shared-services/selected-image-changed-service";
import {Heartbeat} from "./heartbeat";
import {of} from "rxjs";
import {HeartbeatService} from "./heartbeat.service";
import {By} from "@angular/platform-browser";

describe('AppComponent', () => {
  let app: AppComponent;
  let fixture: ComponentFixture<AppComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        HttpClientModule
      ],
      providers: [
        SelectedImageChangedService
      ],
      declarations: [
        AppComponent,
        ImageComponent,
        ImageFilesComponent,
      ],
    }).compileComponents();
    fixture = TestBed.createComponent(AppComponent);
    app = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create the app', () => {
    expect(app).toBeTruthy();
  });

  it(`should have as title 'Frontend'`, () => {
    expect(app.title).toEqual('Object Detection Analyzer');
  });

  it('should render title', () => {
    const compiled = fixture.nativeElement as HTMLElement;

    expect(compiled.querySelector('h1')?.textContent).toEqual(app.title);
  });

  it('should be initialized with heartbeat of 1', () => {
    const heartbeat: Heartbeat = {count: 1};

    expect(app.heartbeat).toEqual(heartbeat);
  })

  it('#getHeartbeat should increment heartbeat', () => {
    const incrementedHeartbeat: Heartbeat = {count: 2};
    const fakeHeartbeat: Heartbeat = {count: 3};
    const heartbeatService = TestBed.inject(HeartbeatService);
    spyOn(heartbeatService, 'getHeartbeat')
      .and.returnValue(of(incrementedHeartbeat));

    app.getHeartbeat();

    expect(app.heartbeat).toBe(incrementedHeartbeat);
    expect(app.heartbeat).not.toBe(fakeHeartbeat);
  });

  it('should render heartbeat', () => {
    expect(fixture.debugElement.query(By.css('#heartbeat')).nativeElement.innerText).toContain(1);
  });

  it('fetch heartbeat in an interval of 5000ms', fakeAsync(() => {
    const spy = spyOn(app, 'getHeartbeat');
    app.ngOnInit();
    tick(5000);
    expect(spy).toHaveBeenCalledTimes(1);
    tick(5000);
    expect(spy).toHaveBeenCalledTimes(2);
    discardPeriodicTasks();
  }));
});
