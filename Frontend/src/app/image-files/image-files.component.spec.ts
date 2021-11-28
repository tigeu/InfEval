import {ComponentFixture, TestBed} from '@angular/core/testing';

import {ImageFilesComponent} from './image-files.component';

describe('ImageFilesComponent', () => {
  let component: ImageFilesComponent;
  let fixture: ComponentFixture<ImageFilesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ImageFilesComponent]
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ImageFilesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
