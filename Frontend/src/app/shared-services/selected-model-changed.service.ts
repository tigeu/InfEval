import {Injectable} from '@angular/core';
import {Observable, Subject} from "rxjs";
import {ModelFile} from "../model-list/model-file";

@Injectable({
  providedIn: 'root'
})
export class SelectedModelChangedService {
  private readonly subjectSource$ = new Subject<ModelFile>();

  public get newData(): Observable<ModelFile> {
    return this.subjectSource$.asObservable();
  }

  public publish(data: ModelFile) {
    this.subjectSource$.next(data);
  }
}
