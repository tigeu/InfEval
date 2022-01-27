import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from "../../environments/environment";
import {Token} from "./Token";
import {CookieService} from "ngx-cookie-service";
import jwtDecode from "jwt-decode";
import {UserLoggedInService} from "../shared-services/user-logged-in-service";

@Injectable({
  providedIn: 'root'
})
export class LoginService {
  private loginUrl = `${environment.apiUrl}/login/`;
  private cookieName: string = 'access';
  jwtDecode = jwtDecode; // for testing

  constructor(private http: HttpClient,
              private cookieService: CookieService,
              private userLoggedInService: UserLoggedInService) {
  }

  login(username: String, password: String) {
    const response = this.http.post<any>(this.loginUrl, {username, password});
    response.subscribe(res => {
      const decoded = this.jwtDecode<Token>(res.access)
      this.cookieService.set(this.cookieName, res.access, decoded.exp)
      this.userLoggedInService.publish(true);
    });

    return response;
  }

  isLoggedIn(): Boolean {
    return this.cookieService.check(this.cookieName);
  }

  getToken(): String {
    if (this.isLoggedIn()) {
      return this.cookieService.get(this.cookieName);
    }

    return "";
  }

  logout(): void {
    if (this.isLoggedIn()) {
      this.cookieService.delete(this.cookieName)
      this.userLoggedInService.publish(false);
    }
  }
}
