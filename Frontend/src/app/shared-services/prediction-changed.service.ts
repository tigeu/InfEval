import {Injectable} from '@angular/core';
import {Observable, Subject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class PredictionChangedService {
  /*
  Shared service for sending the prediction image

  Attributes
  ----------
  subjectSource$ : Subject<object>
    Subject containing the data

  Methods
  -------
  get newData()
    Method used to receive data
  publish(data: any)
    Method used to publish data
  */
  private readonly subjectSource$ = new Subject<object>();

  public get newData(): Observable<object> {
    return this.subjectSource$.asObservable();
  }

  public publish(data: any) {
    this.subjectSource$.next(data);
  }
}
