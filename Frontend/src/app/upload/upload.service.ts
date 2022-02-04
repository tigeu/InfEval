import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class UploadService {
  private uploadUrl = `${environment.apiUrl}/upload`;

  constructor(private http: HttpClient) {
  }

  upload(fileName: String, file: File, datasetName: string, modelName: string, endpoint: string): Observable<any> {
    const queryUrl = `${this.uploadUrl}/${endpoint}/${fileName}`
    const formData = new FormData();
    formData.append("file", file);
    formData.append("dataset_name", datasetName);
    formData.append("model_name", modelName);
    return this.http.put(queryUrl, formData, {reportProgress: true, observe: 'events'})
  }
}
