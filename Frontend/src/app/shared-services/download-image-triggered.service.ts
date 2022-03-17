import {Injectable} from '@angular/core';
import {Observable, Subject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class DownloadImageTriggeredService {
  /*
  Shared service for sending a triggered download

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
  private readonly subjectSource$ = new Subject<boolean>();

  public get newData(): Observable<boolean> {
    return this.subjectSource$.asObservable();
  }

  public publish(data: boolean) {
    this.subjectSource$.next(data);
  }
}
