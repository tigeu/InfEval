import {ComponentFixture, TestBed} from '@angular/core/testing';
import {LoginComponent} from './login.component';
import {HttpClientModule} from "@angular/common/http";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {RouterTestingModule} from "@angular/router/testing";
import {UserLoggedInService} from "../shared-services/user-logged-in-service";
import {LoginService} from "./login.service";
import {Router} from "@angular/router";
import {By} from "@angular/platform-browser";

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

  it('#login should call loginService.login', () => {
    const loginService = TestBed.inject(LoginService);
    spyOn(loginService, "login").withArgs("test", "testPassword");

    component.login("test", "testPassword");

    expect(loginService.login).toHaveBeenCalled();
  });

  it('#onLogin should call login if form is filled', () => {
    spyOn(component, "login").withArgs("test", "testPassword");
    component.loginForm.value.username = "test";
    component.loginForm.value.password = "testPassword";

    component.onLogin();

    expect(component.login).toHaveBeenCalledWith("test", "testPassword");
  });

  it('#onLogin should not call login if form is not filled', () => {
    spyOn(component, "login").withArgs("test", "testPassword");
    component.loginForm.value.username = "";
    component.loginForm.value.password = "";

    component.onLogin();

    expect(component.login).not.toHaveBeenCalled();
  });

  it('#onLoggedIn should route to /', () => {
    const router = TestBed.inject(Router);
    spyOn(router, "navigate").withArgs(['/']);

    component.onLoggedIn();

    expect(router.navigate).toHaveBeenCalled();
  })

  it('should render loginForm', () => {
    expect(fixture.debugElement.query(By.css('#loginForm'))).toBeTruthy();
  });
});
