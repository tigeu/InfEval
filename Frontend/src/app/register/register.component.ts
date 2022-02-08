import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {RegisterService} from "./register.service";
import {Router} from "@angular/router"
import {HttpErrorResponse} from "@angular/common/http";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  registerForm: FormGroup;
  errorMessage: string = "";
  usernameErrorMessage: string = "";
  emailErrorMessage: string = "";
  passwordErrorMessage: string = "";

  constructor(private registerService: RegisterService,
              private formBuilder: FormBuilder,
              private router: Router) {
    this.registerForm = this.formBuilder.group({
      username: ['', Validators.required],
      email: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  onRegister() {
    this.errorMessage = "";
    const value = this.registerForm.value;
    const formValid = this.validateForm(value.username, value.email, value.password);
    if (formValid)
      this.register(value.username, value.email, value.password);
  }

  register(username: String, email: String, password: String) {
    this.registerService.register(username, email, password).subscribe({
      next: this.successfulRegister.bind(this),
      error: this.setResponseErrorMessage.bind(this)
    });
  }

  successfulRegister() {
    this.router.navigate(['/login/'])
  }

  setResponseErrorMessage(res: HttpErrorResponse) {
    let errorMessage = "";
    const usernameError = res.error.username;
    if (usernameError) errorMessage += usernameError
    const emailError = res.error.email;
    if (emailError) errorMessage += "\n" + emailError
    const passwordError = res.error.password;
    if (passwordError) errorMessage += "\n" + passwordError

    this.errorMessage = errorMessage;
  }

  validateForm(username: string, email: string, password: string): boolean {
    const usernameValid = this.validateUserName(username);
    const emailValid = this.validateEmail(email);
    const passwordValid = this.validatePassword(password);
    return usernameValid && emailValid && passwordValid
  }

  validateUserName(username: string): boolean {
    const userRegExp = new RegExp(/^[a-z0-9]+$/i);
    if (!username) {
      this.usernameErrorMessage = "Username missing";
      return false;
    }
    if (username && !userRegExp.test(username)) {
      this.usernameErrorMessage = "Username is not alphanumeric";
      return false;
    }
    this.usernameErrorMessage = "";
    return true;
  }

  validateEmail(email: string): boolean {
    if (!email) {
      this.emailErrorMessage = "Email missing";
      return false;
    }
    const emailRegExp = new RegExp(/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/);
    if (email && !emailRegExp.test(email)) {
      this.emailErrorMessage = "Invalid email";
      return false;
    }
    this.emailErrorMessage = "";
    return true;
  }

  validatePassword(password: string): boolean {
    if (!password) {
      this.passwordErrorMessage = "Password missing";
      return false;
    }
    this.passwordErrorMessage = "";
    return true;
  }

  ngOnInit(): void {

  }

}
