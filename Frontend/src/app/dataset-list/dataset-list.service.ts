import {Injectable} from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {DatasetFile} from "./dataset-file";

@Injectable({
  providedIn: 'root'
})
export class DatasetListService {
  private datasetListUrl = `${environment.apiUrl}/dataset-list`;

  constructor(private http: HttpClient) {
  }

  getDatasetList(): Observable<DatasetFile[]> {
    return this.http.get<DatasetFile[]>(this.datasetListUrl);
  }
}
