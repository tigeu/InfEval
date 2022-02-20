import {Injectable} from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {OverviewFile} from "./overview-file";

@Injectable({
  providedIn: 'root'
})
export class OverviewService {
  private overviewUrl = `${environment.apiUrl}/overview`;

  constructor(private http: HttpClient) {
  }

  getOverviewData(): Observable<OverviewFile> {
    const queryUrl = `${this.overviewUrl}`
    return this.http.get<OverviewFile>(queryUrl);
  }

  deleteDataset(name: string): Observable<any> {
    return this.http.delete(`${environment.apiUrl}/dataset-list/${name}`)
  }

  deletePrediction(name: string): Observable<any> {
    return this.http.delete(`${environment.apiUrl}/prediction-list/${name}`)
  }

  deleteModel(name: string): Observable<any> {
    return this.http.delete(`${environment.apiUrl}/model-list/${name}`)
  }

  deleteTask(name: string): Observable<any> {
    return this.http.delete(`${environment.apiUrl}/tasks-list/${name}`)
  }
}
