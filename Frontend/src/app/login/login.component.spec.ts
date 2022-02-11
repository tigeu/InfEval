import {ComponentFixture, TestBed} from '@angular/core/testing';
import {LoginComponent} from './login.component';
import {HttpClientModule, HttpErrorResponse, HttpResponse} from "@angular/common/http";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {RouterTestingModule} from "@angular/router/testing";
import {UserLoggedInService} from "../shared-services/user-logged-in-service";
import {LoginService} from "./login.service";
import {Router} from "@angular/router";
import {By} from "@angular/platform-browser";
import {of, throwError} from "rxjs";

describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        FormsModule,
        ReactiveFormsModule,
        RouterTestingModule
      ],
      declarations: [LoginComponent]
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('subscription should trigger #onLoggedIn if data is true', () => {
    const userLoggedInService = TestBed.inject(UserLoggedInService);
    spyOn(component, 'onLoggedIn');

    userLoggedInService.publish(true);

    expect(component.onLoggedIn).toHaveBeenCalled();
  });

  it('subscription should not trigger #onLoggedIn if data is false', () => {
    const userLoggedInService = TestBed.inject(UserLoggedInService);
    spyOn(component, 'onLoggedIn');

    userLoggedInService.publish(false);

    expect(component.onLoggedIn).not.toHaveBeenCalled();
  });

  it('should logout user if logged in on navigation', () => {
    const loginService = TestBed.inject(LoginService);
    spyOn(loginService, "isLoggedIn").and.returnValue(true);
    spyOn(loginService, "logout");

    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;

    expect(loginService.logout).toHaveBeenCalled();
  });

  it('should not logout user if not logged in on navigation', () => {
    const loginService = TestBed.inject(LoginService);
    spyOn(loginService, "isLoggedIn").and.returnValue(false);
    spyOn(loginService, "logout");

    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;

    expect(loginService.logout).not.toHaveBeenCalled();
  });

  it('#login should call loginService.login and reset error messages', () => {
    const loginService = TestBed.inject(LoginService);
    spyOn(loginService, "login").withArgs("test", "testPassword")
      .and.returnValue(of(HttpResponse));
    spyOn(component, "resetErrorMessages");

    component.login("test", "testPassword");

    expect(loginService.login).toHaveBeenCalled();
    expect(component.resetErrorMessages).toHaveBeenCalled();
  });

  it('#login should set error message and reset form on error', () => {
    const loginService = TestBed.inject(LoginService);
    spyOn(loginService, "login").withArgs("test", "testPassword")
      .and.returnValue(throwError(() => "error"));
    spyOn(component, "setErrorMessage");

    component.login("test", "testPassword");

    expect(component.setErrorMessage).toHaveBeenCalled();
  });

  it('#onLogin should set error messages and call login if form is filled', () => {
    spyOn(component, "setErrorMessages").withArgs("test", "testPassword");
    spyOn(component, "login").withArgs("test", "testPassword");
    component.loginForm.value.username = "test";
    component.loginForm.value.password = "testPassword";

    component.onLogin();

    expect(component.setErrorMessages).toHaveBeenCalledWith("test", "testPassword");
    expect(component.login).toHaveBeenCalledWith("test", "testPassword");
  });

  it('#onLogin should set error messages and not call login if form is not filled', () => {
    spyOn(component, "setErrorMessages").withArgs("", "");
    spyOn(component, "login").withArgs("test", "testPassword");
    component.loginForm.value.username = "";
    component.loginForm.value.password = "";

    component.onLogin();

    expect(component.setErrorMessages).toHaveBeenCalledWith("", "");
    expect(component.login).not.toHaveBeenCalled();
  });

  it('#onLoggedIn should route to /', () => {
    const router = TestBed.inject(Router);
    spyOn(router, "navigate").withArgs(['/']);

    component.onLoggedIn();

    expect(router.navigate).toHaveBeenCalled();
  });

  it('#resetErrorMessages should reset error messages', () => {
    component.resetErrorMessages();

    expect(component.errorMessage).toEqual("");
    expect(component.usernameErrorMessage).toEqual("");
    expect(component.passwordErrorMessage).toEqual("");
  });

  it('#setErrorMessages should set message for invalid credentials', () => {
    const httpErrorResponse = new HttpErrorResponse({
      error: {detail: "Invalid credentials"},
      status: 400,
      statusText: 'Bad Request'
    })
    spyOn(component.loginForm, "reset");

    component.setErrorMessage(httpErrorResponse);

    expect(component.errorMessage).toEqual("Invalid credentials");
    expect(component.loginForm.reset).toHaveBeenCalled();
  });

  it('#setErrorMessages should set missing message for missing attributes', () => {
    component.setErrorMessages("", "");

    expect(component.usernameErrorMessage).toEqual("Username missing");
    expect(component.passwordErrorMessage).toEqual("Password missing");
  });

  it('should render loginForm', () => {
    expect(fixture.debugElement.query(By.css('#loginForm'))).toBeTruthy();
  });

  it('#ngOnDestroy unsubscribes from all subscriptions', () => {
    const userLoggedInSpy = spyOn(component.userLoggedIn, 'unsubscribe');

    component.ngOnDestroy();

    expect(userLoggedInSpy).toHaveBeenCalled();
  });
});
