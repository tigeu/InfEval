import {Injectable} from '@angular/core';
import {Observable, Subject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class UserLoggedInService {
  /*
  Shared service for sending a user login event

  Attributes
  ----------
  subjectSource$ : Subject<boolean>
    Subject containing the data

  Methods
  -------
  get newData()
    Method used to receive data
  publish(data: boolean)
    Method used to publish data
  */
  private readonly subjectSource$ = new Subject<Boolean>();

  public get newData(): Observable<Boolean> {
    return this.subjectSource$.asObservable();
  }

  public publish(data: Boolean) {
    this.subjectSource$.next(data);
  }
}
