import {Injectable} from '@angular/core';
import {Observable, Subject} from "rxjs";

@Injectable()
export class SelectedImageChangedService {
  private readonly subjectSource$ = new Subject<object>();

  public get newData(): Observable<object> {
    return this.subjectSource$.asObservable();
  }

  public publish(data: any) {
    this.subjectSource$.next(data);
  }
}
