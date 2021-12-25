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

  upload(fileName: String, file: File, type: string): Observable<any> {
    const queryUrl = `${this.uploadUrl}/${fileName}`
    const formData = new FormData();
    formData.append("file", file);
    formData.append("type", type);
    return this.http.put(queryUrl, formData, {reportProgress: true, observe: 'events'})
  }
}
