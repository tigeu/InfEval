import {Injectable} from '@angular/core';
import {Observable, Subject} from "rxjs";
import {DatasetFile} from "../dataset-list/dataset-file";

@Injectable({
  providedIn: 'root'
})
export class SelectedDatasetChangedService {
  private readonly subjectSource$ = new Subject<DatasetFile>();

  public get newData(): Observable<DatasetFile> {
    return this.subjectSource$.asObservable();
  }

  public publish(data: DatasetFile) {
    this.subjectSource$.next(data);
  }
}
