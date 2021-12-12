import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {RegisterService} from "./register.service";
import {Router} from "@angular/router"

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  registerForm: FormGroup;

  constructor(private registerService: RegisterService,
              private formBuilder: FormBuilder,
              private router: Router) {
    this.registerForm = this.formBuilder.group({
      username: ['', Validators.required],
      email: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  register(username: String, email: String, password: String) {
    this.registerService.register(username, email, password).subscribe({
      next: this.successfulRegister.bind(this)
    });
  }

  successfulRegister() {
    this.router.navigate(['/login/'])
  }

  ngOnInit(): void {
  }

  onRegister() {
    this.register(this.registerForm.value.username, this.registerForm.value.email, this.registerForm.value.password);
  }

}
