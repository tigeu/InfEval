import {Injectable} from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class RegisterService {
  private registerUrl = `${environment.apiUrl}/register/`;

  constructor(private http: HttpClient) {
  }

  register(username: String, email: String, password: String): Observable<any> {
    console.log(this.registerUrl)
    console.log(username, email, password)
    return this.http.post(this.registerUrl, {
      "username": username,
      "email": email,
      "password": password
    });
  }
}
