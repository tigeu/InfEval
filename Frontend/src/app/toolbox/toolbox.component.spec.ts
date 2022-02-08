import {ComponentFixture, TestBed} from '@angular/core/testing';

import {ToolboxComponent} from './toolbox.component';
import {GroundTruthComponent} from "../ground-truth/ground-truth.component";
import {HttpClientModule} from "@angular/common/http";
import {DownloadImageTriggeredService} from "../shared-services/download-image-triggered.service";
import {SelectedImageChangedService} from "../shared-services/selected-image-changed-service";
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

  it('click should call startDownload promise', () => {
    spyOn(component, 'startDownload');

    component.downloadTriggered();

    expect(component.startDownload).toHaveBeenCalled();
  });

  it('expect startDownload to be awaited', async () => {
    await expectAsync(component.downloadTriggered()).toBeResolved();
  })

  it('download subscription should reset isDownloading', () => {
    const downloadImageTriggeredService = TestBed.inject(DownloadImageTriggeredService);

    downloadImageTriggeredService.publish(false);

    expect(component.isDownloading).not.toBeTruthy();
  });

  it('image subscription should set imageSelected', () => {
    const selectedImageChangedService = TestBed.inject(SelectedImageChangedService);

    selectedImageChangedService.publish("some data");

    expect(component.imageSelected).toEqual(true);
  });

  it('image subscription should unset imageSelected', () => {
    const selectedImageChangedService = TestBed.inject(SelectedImageChangedService);

    selectedImageChangedService.publish("");

    expect(component.imageSelected).toEqual(false);
  });

  it('#ngOnDestroy unsubscribes from all subscriptions', () => {
    const selectedImageChangedSpy = spyOn(component.selectedImageChanged, 'unsubscribe');

    component.ngOnDestroy();

    expect(selectedImageChangedSpy).toHaveBeenCalled();
  });
});
