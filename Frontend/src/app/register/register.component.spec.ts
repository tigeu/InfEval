import {ComponentFixture, TestBed} from '@angular/core/testing';

import {RegisterComponent} from './register.component';
import {HttpClientModule, HttpResponse} from "@angular/common/http";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {RouterTestingModule} from "@angular/router/testing";
import {RegisterService} from "./register.service";
import {of} from "rxjs";
import {Router} from "@angular/router";

describe('RegisterComponent', () => {
  let component: RegisterComponent;
  let fixture: ComponentFixture<RegisterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        FormsModule,
        ReactiveFormsModule,
        RouterTestingModule
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

  it('#successfulRegister should navigate to /login/', () => {
    const router = TestBed.inject(Router);
    spyOn(router, "navigate").withArgs(['/login/']);

    component.successfulRegister();

    expect(router.navigate).toHaveBeenCalled();
  });

  it('#onRegister should call register if form is filled', () => {
    spyOn(component, "register").withArgs("test", "testEmail", "testPassword");
    component.registerForm.value.username = "test";
    component.registerForm.value.email = "testEmail";
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
