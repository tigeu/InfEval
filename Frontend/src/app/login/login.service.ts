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

  constructor(private http: HttpClient,
              private cookieService: CookieService,
              private userLoggedInService: UserLoggedInService) {
  }

  login(username: String, password: String) {
    this.http.post<any>(this.loginUrl, {username, password}).subscribe(res => {
      const decoded = jwtDecode<Token>(res.access)
      this.cookieService.set(this.cookieName, res.access, decoded.exp)
      this.userLoggedInService.publish(true);
    });
  }

  isLoggedIn(): Boolean {
    return this.cookieService.check(this.cookieName);
  }

  getToken(): String {
    if (this.isLoggedIn()) {
      return this.cookieService.get('access');
    }

    return "";
  }

  logout(): void {
    this.cookieService.delete(this.cookieName)
    this.userLoggedInService.publish(false);
  }
}
