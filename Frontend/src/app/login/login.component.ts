import {Component, OnInit} from '@angular/core';
import {LoginService} from "./login.service";
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {Router} from "@angular/router"
import {Subscription} from "rxjs";
import {UserLoggedInService} from "../shared-services/user-logged-in-service";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  private userLoggedIn: Subscription;

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

  login(username: String, password: String) {
    this.loginService.login(username, password);
  }

  ngOnInit(): void {
  }

  onLogin() {
    const value = this.loginForm.value;
    if (value.username && value.password)
      this.login(value.username, value.password);
  }

  onLoggedIn() {
    this.router.navigate(['/'])
  }
}
