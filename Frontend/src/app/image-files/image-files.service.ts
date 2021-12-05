import {Injectable} from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from '@angular/common/http';
import {environment} from "../../environments/environment";
import {ImageFile} from "./image-file";

@Injectable({
  providedIn: 'root'
})
export class ImageFilesService {
  private imageFilesUrl = `${environment.apiUrl}/image-files/`;

  constructor(private http: HttpClient) {
  }

  getImageFiles(): Observable<ImageFile[]> {
    return this.http.get<ImageFile[]>(this.imageFilesUrl);
  }
}
