import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {HttpClientModule} from '@angular/common/http';
import {ImageComponent} from './image/image.component';
import {ImageFilesComponent} from './image-files/image-files.component';
import {SelectedImageChangedService} from "./shared-services/selected-image-changed-service";

@NgModule({
  declarations: [
    AppComponent,
    ImageComponent,
    ImageFilesComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
  ],
  providers: [
    SelectedImageChangedService
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
