import {TestBed} from '@angular/core/testing';

import {HttpClient} from "@angular/common/http";

import {HttpClientTestingModule} from "@angular/common/http/testing";
import {of} from "rxjs";
import {LoginService} from "./login.service";
import {UserLoggedInService} from "../shared-services/user-logged-in-service";
import {CookieService} from "ngx-cookie-service";

describe('LoginService', () => {
  let service: LoginService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
      ],
      providers: []
    });
    service = TestBed.inject(LoginService);
  });

  it('should be created', () => {
    service = TestBed.inject(LoginService);

    expect(service).toBeTruthy();
  });

  it('#login should create cookie and publish login', () => {
    const http = TestBed.inject(HttpClient);
    const cookieService = TestBed.inject(CookieService);
    const userLoggedInService = TestBed.inject(UserLoggedInService);

    spyOn(http, 'post').and.returnValue(of({'access': 'accessToken'}));
    spyOn(service, "jwtDecode").and.returnValue({'exp': {'expires': 1000}});
    spyOn(cookieService, "set").withArgs('access', 'accessToken', {'expires': 1000});
    spyOn(userLoggedInService, "publish").withArgs(true)

    service.login("test", "test");

    expect(cookieService.set).toHaveBeenCalled()
    expect(userLoggedInService.publish).toHaveBeenCalled();
  });

  it('#isLoggedIn should return true if user is logged in', () => {
    const cookieService = TestBed.inject(CookieService);
    spyOn(cookieService, "check").withArgs('access').and.returnValue(true);

    const result = service.isLoggedIn();

    expect(result).toBe(true);
  });

  it('#isLoggedIn should return false if user is not logged in', () => {
    const cookieService = TestBed.inject(CookieService);
    spyOn(cookieService, "check").withArgs('access').and.returnValue(false);

    const result = service.isLoggedIn();

    expect(result).toBe(false);
  });

  it('#getToken should return current cookie if logged in', () => {
    const cookieService = TestBed.inject(CookieService);

    spyOn(service, "isLoggedIn").and.returnValue(true);
    spyOn(cookieService, "get").withArgs('access').and.returnValue('accessToken');

    const result = service.getToken();

    expect(result).toBe('accessToken')
  });

  it('#getToken should return emptry string if not logged in', () => {
    spyOn(service, "isLoggedIn").and.returnValue(false);

    const result = service.getToken();

    expect(result).toBe('')
  });

  it('#logout should delete cookie and publish logout if logged in', () => {
    const cookieService = TestBed.inject(CookieService);
    const userLoggedInService = TestBed.inject(UserLoggedInService);

    spyOn(service, "isLoggedIn").and.returnValue(true);
    spyOn(cookieService, "delete").withArgs('access');
    spyOn(userLoggedInService, "publish").withArgs(false);

    service.logout();

    expect(cookieService.delete).toHaveBeenCalled();
    expect(userLoggedInService.publish).toHaveBeenCalled();
  })

  it('#logout should do nothing if not logged in', () => {
    const cookieService = TestBed.inject(CookieService);
    const userLoggedInService = TestBed.inject(UserLoggedInService);

    spyOn(service, "isLoggedIn").and.returnValue(false);
    spyOn(cookieService, "delete");
    spyOn(userLoggedInService, "publish");

    expect(cookieService.delete).not.toHaveBeenCalled();
    expect(userLoggedInService.publish).not.toHaveBeenCalled();
  })
})
