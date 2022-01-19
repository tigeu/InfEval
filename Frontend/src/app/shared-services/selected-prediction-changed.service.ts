import {Injectable} from '@angular/core';
import {Observable, Subject} from "rxjs";
import {PredictionFile} from "../prediction-list/prediction-file";

@Injectable({
  providedIn: 'root'
})
export class SelectedPredictionChangedService {
  private readonly subjectSource$ = new Subject<PredictionFile>();

  public get newData(): Observable<PredictionFile> {
    return this.subjectSource$.asObservable();
  }

  public publish(data: PredictionFile) {
    this.subjectSource$.next(data);
  }
}
