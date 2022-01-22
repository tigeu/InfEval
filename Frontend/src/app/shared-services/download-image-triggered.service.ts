import {Injectable} from '@angular/core';
import {Observable, Subject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class DownloadImageTriggeredService {
  private readonly subjectSource$ = new Subject<boolean>();

  public get newData(): Observable<boolean> {
    return this.subjectSource$.asObservable();
  }

  public publish(data: boolean) {
    this.subjectSource$.next(data);
  }
}
