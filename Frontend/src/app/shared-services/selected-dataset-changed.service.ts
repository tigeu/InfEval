import {Injectable} from '@angular/core';
import {Observable, Subject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class SelectedDatasetChangedService {
  private readonly subjectSource$ = new Subject<string>();

  public get newData(): Observable<string> {
    return this.subjectSource$.asObservable();
  }

  public publish(data: string) {
    this.subjectSource$.next(data);
  }
}
