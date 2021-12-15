import {TestBed} from '@angular/core/testing';
import {HttpClientTestingModule} from "@angular/common/http/testing";
import {UserLoggedInService} from "./user-logged-in-service";

describe('UserLoggedInService', () => {
  let service: UserLoggedInService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
      ],
      providers: []
    });
    service = TestBed.inject(UserLoggedInService);
  });

  it('should be created', () => {
    service = TestBed.inject(UserLoggedInService);

    expect(service).toBeTruthy();
  });

  it('#newData should return published login', () => {
    // assert before act
    service.newData.subscribe((data: any) => {
      expect(data).toBe(true)
    });

    service.publish(true);
  });

  it('#newData should return published logout', () => {
    // assert before act
    service.newData.subscribe((data: any) => {
      expect(data).toBe(false)
    });

    service.publish(false);
  });
})
