import {ComponentFixture, TestBed} from '@angular/core/testing';

import {RegisterComponent} from './register.component';
import {HttpClientModule, HttpErrorResponse, HttpResponse} from "@angular/common/http";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {RouterTestingModule} from "@angular/router/testing";
import {RegisterService} from "./register.service";
import {of, throwError} from "rxjs";
import {Router} from "@angular/router";
import {MatSelectModule} from "@angular/material/select";

describe('RegisterComponent', () => {
  let component: RegisterComponent;
  let fixture: ComponentFixture<RegisterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        FormsModule,
        ReactiveFormsModule,
        RouterTestingModule,
        MatSelectModule
      ],
      declarations: [RegisterComponent]
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RegisterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#register should call successfulRegister on valid response', () => {
    const registerService = TestBed.inject(RegisterService);
    spyOn(registerService, "register").withArgs("test", "testEmail", "testPassword")
      .and.returnValue(of(new HttpResponse<any>()));
    spyOn(component, "successfulRegister");

    component.register("test", "testEmail", "testPassword");

    expect(component.successfulRegister).toHaveBeenCalled();
  });

  it('#register should call setResponseErrorMessage on invalid response', () => {
    const registerService = TestBed.inject(RegisterService);
    spyOn(registerService, "register").withArgs("test", "testEmail", "testPassword")
      .and.returnValue(throwError(() => "error"));
    spyOn(component, "setResponseErrorMessage");

    component.register("test", "testEmail", "testPassword");

    expect(component.setResponseErrorMessage).toHaveBeenCalled();
  });

  it('#successfulRegister should navigate to /login/', () => {
    const router = TestBed.inject(Router);
    spyOn(router, "navigate").withArgs(['/login/']);

    component.successfulRegister();

    expect(router.navigate).toHaveBeenCalled();
  });

  it('#setResponseErrorMessage should set error messages', () => {
    const httpErrorResponse = new HttpErrorResponse({
      error: {username: "Invalid username", email: "Invalid email", password: "Invalid password"},
      status: 400,
      statusText: 'Bad Request'
    })

    component.setResponseErrorMessage(httpErrorResponse);

    expect(component.errorMessage).toEqual("Invalid username\nInvalid email\nInvalid password");
  });

  it('#validateForm should call validation methods', () => {
    spyOn(component, "validateUserName").withArgs("user");
    spyOn(component, "validateEmail").withArgs("email");
    spyOn(component, "validatePassword").withArgs("password");

    component.validateForm("user", "email", "password");

    expect(component.validateUserName).toHaveBeenCalled();
    expect(component.validatePassword).toHaveBeenCalled();
    expect(component.validatePassword).toHaveBeenCalled();
  });

  it('#validateUserName should return true and reset message if valid', () => {
    const result = component.validateUserName("validUsername");

    expect(result).toBeTruthy();
    expect(component.usernameErrorMessage).toEqual("");
  });

  it('#validateUserName should return false if no username and set message', () => {
    const result = component.validateUserName("");

    expect(result).not.toBeTruthy();
    expect(component.usernameErrorMessage).toEqual("Username missing");
  });

  it('#validateUserName should return false if no alphanumeric username and set message', () => {
    const result = component.validateUserName("<<>><><>!!!!");

    expect(result).not.toBeTruthy();
    expect(component.usernameErrorMessage).toEqual("Username is not alphanumeric");
  });

  it('#validateEmail should return true and reset message if valid', () => {
    const result = component.validateEmail("valid@e.mail");

    expect(result).toBeTruthy();
    expect(component.emailErrorMessage).toEqual("");
  });

  it('#validateEmail should return false if no email and set message', () => {
    const result = component.validateEmail("");

    expect(result).not.toBeTruthy();
    expect(component.emailErrorMessage).toEqual("Email missing");
  });

  it('#validateEmail should return false if email is invalid', () => {
    const result = component.validateEmail("invalid@email");

    expect(result).not.toBeTruthy();
    expect(component.emailErrorMessage).toEqual("Invalid email");
  });

  it('#validatePassword should return true and reset message if valid', () => {
    const result = component.validatePassword("valid@e.mail");

    expect(result).toBeTruthy();
    expect(component.passwordErrorMessage).toEqual("");
  });

  it('#validatePassword should return false if no password and set message', () => {
    const result = component.validatePassword("");

    expect(result).not.toBeTruthy();
    expect(component.passwordErrorMessage).toEqual("Password missing");
  });

  it('#onRegister should call register if form is filled', () => {
    spyOn(component, "register").withArgs("test", "testEmail@test.test", "testPassword");
    component.registerForm.value.username = "test";
    component.registerForm.value.email = "testEmail@test.test";
    component.registerForm.value.password = "testPassword";

    component.onRegister();

    expect(component.register).toHaveBeenCalled();
  });

  it('#onRegister should not call register if form is not filled', () => {
    spyOn(component, "register").withArgs("test", "testEmail", "testPassword");
    component.registerForm.value.username = "";
    component.registerForm.value.email = "";
    component.registerForm.value.password = "";

    component.onRegister();

    expect(component.register).not.toHaveBeenCalled();
  });
});
