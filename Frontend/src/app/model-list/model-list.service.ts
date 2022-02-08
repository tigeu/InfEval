import {Injectable} from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {ModelFile} from "./model-file";

@Injectable({
  providedIn: 'root'
})
export class ModelListService {
  private modelListUrl = `${environment.apiUrl}/model-list`;

  constructor(private http: HttpClient) {
  }

  getModelList(): Observable<ModelFile[]> {
    const queryUrl = `${this.modelListUrl}`
    return this.http.get<ModelFile[]>(queryUrl);
  }
}
