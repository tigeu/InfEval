import {Injectable} from '@angular/core';
import {Observable, Subject} from "rxjs";
import {DatasetFile} from "../dataset-list/dataset-file";

@Injectable({
  providedIn: 'root'
})
export class SelectedDatasetChangedService {
  /*
  Shared service for sending the selected dataset

  Attributes
  ----------
  subjectSource$ : Subject<DatasetFile>
    Subject containing the data

  Methods
  -------
  get newData()
    Method used to receive data
  publish(data: DatasetFile)
    Method used to publish data
  */
  private readonly subjectSource$ = new Subject<DatasetFile>();

  public get newData(): Observable<DatasetFile> {
    return this.subjectSource$.asObservable();
  }

  public publish(data: DatasetFile) {
    this.subjectSource$.next(data);
  }
}
