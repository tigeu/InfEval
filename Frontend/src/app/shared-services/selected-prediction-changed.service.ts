import {Injectable} from '@angular/core';
import {Observable, Subject} from "rxjs";
import {PredictionFile} from "../prediction-list/prediction-file";

@Injectable({
  providedIn: 'root'
})
export class SelectedPredictionChangedService {
  /*
  Shared service for sending the selected prediction

  Attributes
  ----------
  subjectSource$ : Subject<PredictionFile>
    Subject containing the data

  Methods
  -------
  get newData()
    Method used to receive data
  publish(data: PredictionFile)
    Method used to publish data
  */
  private readonly subjectSource$ = new Subject<PredictionFile>();

  public get newData(): Observable<PredictionFile> {
    return this.subjectSource$.asObservable();
  }

  public publish(data: PredictionFile) {
    this.subjectSource$.next(data);
  }
}
