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
  errorMessage: string = "";
  usernameErrorMessage: string = "";
  passwordErrorMessage: string = "";
  loginForm: FormGroup;
  userLoggedIn: Subscription;

  constructor(private loginService: LoginService,
              private formBuilder: FormBuilder,
              private router: Router,
              private userLoggedInService: UserLoggedInService) {
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
    this.userLoggedIn.unsubscribe();
  }

  login(username: String, password: String) {
    this.loginService.login(username, password).subscribe({
      next: () => {
        this.resetErrorMessages();
      },
      error: this.setErrorMessage.bind(this)
    });
  }

  resetErrorMessages() {
    this.errorMessage = "";
    this.usernameErrorMessage = "";
    this.passwordErrorMessage = "";
  }

  setErrorMessage(res: HttpErrorResponse) {
    this.errorMessage = res.error.detail;
    this.loginForm.reset();
  }

  setErrorMessages(username: string, password: string) {
    this.errorMessage = "";
    if (!username)
      this.usernameErrorMessage = "Username missing";
    if (!password)
      this.passwordErrorMessage = "Password missing";
  }

  onLogin() {
    const value = this.loginForm.value;
    this.setErrorMessages(value.username, value.password);

    if (value.username && value.password) {
      this.resetErrorMessages();
      this.login(value.username, value.password);
    }
  }

  onLoggedIn() {
    this.router.navigate(['/'])
  }
}
