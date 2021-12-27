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

  upload(fileName: String, file: File, dataset_name: string, endpoint: string): Observable<any> {
    const queryUrl = `${this.uploadUrl}/${endpoint}/${fileName}`
    const formData = new FormData();
    formData.append("file", file);
    formData.append("dataset_name", dataset_name)
    return this.http.put(queryUrl, formData, {reportProgress: true, observe: 'events'})
  }
}
