import {Injectable} from '@angular/core';
import {HttpErrorResponse, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {catchError, map, Observable, throwError} from 'rxjs';
import {environment} from "../../environments/environment";
import {LoginService} from "../login/login.service";
import {Router} from "@angular/router";

@Injectable()
export class JwtInterceptor implements HttpInterceptor {
  constructor(private loginService: LoginService, private router: Router) {
  }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const isLoggedIn = this.loginService.isLoggedIn();
    const isApiUrl = request.url.startsWith(environment.apiUrl);
    if (isLoggedIn && isApiUrl) {
      request = request.clone({
        setHeaders: {"Authorization": `Bearer ${this.loginService.getToken()}`}
      });
    }

    return next.handle(request).pipe(
      map((event: HttpEvent<any>) => event),
      catchError((error: HttpErrorResponse) => {
        if (error && error.status == 401) {
          console.log("Redirecting to login page");
          this.router.navigate(['/login']);
        }
        return throwError(() => error);
      }));
  }
}
