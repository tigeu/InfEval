import {Component, OnInit} from '@angular/core';
import {LoginService} from "./login.service";
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {Router} from "@angular/router"
import {Subscription} from "rxjs";
import {UserLoggedInService} from "../shared-services/user-logged-in-service";
import {HttpErrorResponse} from "@angular/common/http";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  /*
  Component that is used to login a user.

  Attributes
  ----------
  loginService : LoginService
    Service used to login a user
  formBuilder : FormBuilder
    FormBuilder used to build the login form
  router : Router
    Router used to navigate to main view
  userLoggedInService : UserLoggedInService
    Service for publishing the login of a user
  errorMessage : string
    Error message from last request
  usernameErrorMessage : string
    Error message from validating username
  passwordErrorMessage : string
    Error message from validating password
  loginForm : FormGroup
    Login form group
  userLoggedIn : Subscription
    Subscription to get login event

  Methods
  -------
  login(username: String, password: String)
    Calls service to login the user with current credentials
  resetErrorMessages()
    Reset all error messages
  setErrorMessage(res: HttpErrorResponse)
    Set login error message and reset the form
  setErrorMessages(username: string, password: string)
    Set error messages for missing entries
  onLogin()
    Validates the filled out form and initiates login
  onLoggedIn()
    Redirect to main view
  */
  errorMessage: string = "";
  usernameErrorMessage: string = "";
  passwordErrorMessage: string = "";
  loginForm: FormGroup;
  userLoggedIn: Subscription;

  constructor(private loginService: LoginService,
              private formBuilder: FormBuilder,
              private router: Router,
              private userLoggedInService: UserLoggedInService) {
    /*
    Initialise loginform and subscription for retrieving user logged in event. If user is already
    login in, log out user.

    Parameters
    ----------
    loginService : LoginService
       Service used to login a user
     formBuilder : FormBuilder
       FormBuilder used to build the login form
     router : Router
       Router used to navigate to main view
     userLoggedInService : UserLoggedInService
       Service for publishing the login of a user
    */
    this.userLoggedIn = this.userLoggedInService.newData.subscribe((data: any) => {
      if (data)
        this.onLoggedIn()
    })

    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });

    if (this.loginService.isLoggedIn())
      this.loginService.logout();
  }

  ngOnInit(): void {
  }

  ngOnDestroy(): void {
    /*
    Unsubscribe from all subscriptions
    */
    this.userLoggedIn.unsubscribe();
  }

  login(username: String, password: String) {
    /*
    Calls service to login the user with current credentials

    Parameters
    ----------
    username : String
      Name of current user
    password : String
      Entered password of user
    */
    this.loginService.login(username, password).subscribe({
      next: () => {
        this.resetErrorMessages();
      },
      error: this.setErrorMessage.bind(this)
    });
  }

  resetErrorMessages() {
    /*
    Reset all error messages
    */
    this.errorMessage = "";
    this.usernameErrorMessage = "";
    this.passwordErrorMessage = "";
  }

  setErrorMessage(res: HttpErrorResponse) {
    /*
    Set login error message and reset the form

    Parameters
    ----------
    res : HttpErrorResponse
      Response containing errors from backend
    */
    this.errorMessage = res.error.detail;
    this.loginForm.reset();
  }

  setErrorMessages(username: string, password: string) {
    /*
    Set error messages for missing entries

    Parameters
    ----------
    username : string
      Entered username
    password : string
      Entered password
    */
    this.errorMessage = "";
    if (!username)
      this.usernameErrorMessage = "Username missing";
    if (!password)
      this.passwordErrorMessage = "Password missing";
  }

  onLogin() {
    /*
    Validates the filled out form and initiates login
    */
    const value = this.loginForm.value;
    this.setErrorMessages(value.username, value.password);

    if (value.username && value.password) {
      this.resetErrorMessages();
      this.login(value.username, value.password);
    }
  }

  onLoggedIn() {
    /*
    Redirect to main view
    */
    this.router.navigate(['/'])
  }
}
