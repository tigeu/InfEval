import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {HTTP_INTERCEPTORS, HttpClientModule} from '@angular/common/http';
import {ImageComponent} from './image/image.component';
import {ImageFilesComponent} from './image-files/image-files.component';
import {LoginComponent} from './login/login.component';
import {CookieService} from 'ngx-cookie-service';
import {JwtInterceptor} from "./login/JwtInterceptor";
import {RegisterComponent} from './register/register.component';
import {MainComponent} from './main/main.component';
import {ReactiveFormsModule} from "@angular/forms";

@NgModule({
  declarations: [
    AppComponent,
    ImageComponent,
    ImageFilesComponent,
    LoginComponent,
    RegisterComponent,
    MainComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule
  ],
  providers: [
    CookieService,
    {provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true}
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
