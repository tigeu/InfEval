import {Injectable} from '@angular/core';
import {Observable, Subject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class UserLoggedInService {
  private readonly subjectSource$ = new Subject<Boolean>();

  public get newData(): Observable<Boolean> {
    return this.subjectSource$.asObservable();
  }

  public publish(data: Boolean) {
    this.subjectSource$.next(data);
  }
}
