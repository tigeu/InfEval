import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment";
import {Observable} from "rxjs";
import {UploadTypes} from "./UploadTypes";

@Injectable({
  providedIn: 'root'
})
export class UploadService {
  private uploadUrl = `${environment.apiUrl}/upload`;

  constructor(private http: HttpClient) {
  }

  upload(fileName: String, file: File, type: UploadTypes): Observable<any> {
    const queryUrl = `${this.uploadUrl}/${fileName}`
    const formData = new FormData();
    formData.append("file", file);
    formData.append("type", type.toString());
    return this.http.put(queryUrl, formData, {reportProgress: true, observe: 'events'})
  }
}
