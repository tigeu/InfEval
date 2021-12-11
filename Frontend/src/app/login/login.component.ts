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
              private userLoggedInService: UserLoggedInService,) {
    this.userLoggedIn = this.userLoggedInService.newData.subscribe((data: any) => {
      if (data)
        this.onLoggedIn()
    })

    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  login(username: String, password: String) {
    this.loginService.login(username, password);
  }

  ngOnInit(): void {
  }

  onLogin() {
    this.login(this.loginForm.value.username, this.loginForm.value.password);
  }

  onLoggedIn() {
    this.router.navigate(['/'])
  }
}
