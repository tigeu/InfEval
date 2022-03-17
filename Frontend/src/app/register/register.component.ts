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
  /*
  Component that is used to register a user.

  Attributes
  ----------
  registerService : RegisterService
    Service used to login a user
  formBuilder : FormBuilder
    FormBuilder used to build the login form
  router : Router
    Router used to navigate to main view
  registerForm : FormGroup
    Register form group
  errorMessage : string
    Error message from last request
  usernameErrorMessage : string
    Error message from validating username
  emailErrorMessage : string
    Error message from validating email
  passwordErrorMessage : string
    Error message from validating password

  Methods
  -------
  onRegister()
    Validates the filled out form and initiates registration
  register(username: String, email: String, password: String)
    Calls service to register the user with current credentials
  successfulRegister()
    Navigate to login view
  setResponseErrorMessage(res: HttpErrorResponse)
    Set error messages from backend for each field
  validateForm(username: string, email: string, password: string)
    Call validation methods for username, email and password
  validateUserName(username: string)
    Validate username (not empty, alphanumeric)
  validateEmail(email: string)
    Validate email (not empty, email regex)
  validatePassword(password: string)
    Validate password (not empty)
  */

  registerForm: FormGroup;
  errorMessage: string = "";
  usernameErrorMessage: string = "";
  emailErrorMessage: string = "";
  passwordErrorMessage: string = "";

  constructor(private registerService: RegisterService,
              private formBuilder: FormBuilder,
              private router: Router) {
    /*
    Initialise registration form

    Parameters
    ----------
    registerService : RegisterService
      Service used to login a user
    formBuilder : FormBuilder
      FormBuilder used to build the login form
    router : Router
      Router used to navigate to main view
    */
    this.registerForm = this.formBuilder.group({
      username: ['', Validators.required],
      email: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  onRegister() {
    /*
    Validates the filled out form and initiates registration
    */
    this.errorMessage = "";
    const value = this.registerForm.value;
    const formValid = this.validateForm(value.username, value.email, value.password);
    if (formValid)
      this.register(value.username, value.email, value.password);
  }

  register(username: String, email: String, password: String) {
    /*
    Calls service to register the user with current credentials

    Parameters
    ----------
    username : String
      Entered username
    email : String
      Entered email
    password : String
      Entered password
    */
    this.registerService.register(username, email, password).subscribe({
      next: this.successfulRegister.bind(this),
      error: this.setResponseErrorMessage.bind(this)
    });
  }

  successfulRegister() {
    /*
    Navigate to login view
    */
    this.router.navigate(['/login/'])
  }

  setResponseErrorMessage(res: HttpErrorResponse) {
    /*
    Set error messages from backend for each field

    Parameters
    ----------
    res : HttpErrorResponse
      Error response containing all errors from field
    */
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
    /*
    Call validation methods for username, email and password

    Parameters
    ----------
    username : string
      Entered username
    email : string
      Entered email
    password : string
      Entered password
    */
    const usernameValid = this.validateUserName(username);
    const emailValid = this.validateEmail(email);
    const passwordValid = this.validatePassword(password);
    return usernameValid && emailValid && passwordValid
  }

  validateUserName(username: string): boolean {
    /*
    Validate username (not empty, alphanumeric)

    Parameters
    ----------
    username : string
      Entered username
    */
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
    /*
    Validate email (not empty, email regex)

    Parameters
    ----------
    email : string
      Entered email
    */
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
    /*
    Validate password (not empty)

    Parameters
    ----------
    password : string
      Entered password
    */
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
