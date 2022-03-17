import {Injectable} from '@angular/core';
import {Observable, Subject} from "rxjs";
import {ModelFile} from "../model-list/model-file";

@Injectable({
  providedIn: 'root'
})
export class SelectedModelChangedService {
  /*
  Shared service for sending the selected model

  Attributes
  ----------
  subjectSource$ : Subject<ModelFile>
    Subject containing the data

  Methods
  -------
  get newData()
    Method used to receive data
  publish(data: ModelFile)
    Method used to publish data
  */
  private readonly subjectSource$ = new Subject<ModelFile>();

  public get newData(): Observable<ModelFile> {
    return this.subjectSource$.asObservable();
  }

  public publish(data: ModelFile) {
    this.subjectSource$.next(data);
  }
}
