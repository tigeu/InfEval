import {Injectable} from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {PredictionFile} from "./prediction-file";

@Injectable({
  providedIn: 'root'
})
export class PredictionListService {
  private predictionListUrl = `${environment.apiUrl}/prediction-list`;

  constructor(private http: HttpClient) {
  }

  getPredictionList(dataset: string): Observable<PredictionFile[]> {
    const queryUrl = `${this.predictionListUrl}/${dataset}`
    return this.http.get<PredictionFile[]>(queryUrl);
  }
}
