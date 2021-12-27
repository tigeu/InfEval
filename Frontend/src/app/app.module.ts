import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {HTTP_INTERCEPTORS, HttpClientModule} from '@angular/common/http';
import {ImageComponent} from './image/image.component';
import {ImageFilesComponent} from './image-files/image-files.component';
import {LoginComponent} from './login/login.component';
import {CookieService} from 'ngx-cookie-service';
import {JwtInterceptor} from "./interceptors/jwt-interceptor";
import {RegisterComponent} from './register/register.component';
import {MainComponent} from './main/main.component';
import {ReactiveFormsModule} from "@angular/forms";
import {UploadComponent} from './upload/upload.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatProgressBarModule} from "@angular/material/progress-bar";
import {MatIconModule} from "@angular/material/icon";
import {MatButtonModule} from "@angular/material/button";
import {UploadMainComponent} from './upload-main/upload-main.component';
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatTabsModule} from "@angular/material/tabs";
import {DatasetListComponent} from './dataset-list/dataset-list.component';
import {MatSelectModule} from "@angular/material/select";

@NgModule({
  declarations: [
    AppComponent,
    ImageComponent,
    ImageFilesComponent,
    LoginComponent,
    RegisterComponent,
    MainComponent,
    UploadComponent,
    UploadMainComponent,
    DatasetListComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    MatProgressBarModule,
    MatIconModule,
    MatButtonModule,
    MatFormFieldModule,
    MatTabsModule,
    MatSelectModule
  ],
  providers: [
    CookieService,
    {provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true}
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
