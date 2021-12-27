import {Injectable} from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from '@angular/common/http';
import {environment} from "../../environments/environment";
import {ImageFile} from "./image-file";

@Injectable({
  providedIn: 'root'
})
export class ImageFilesService {
  private imageFilesUrl = `${environment.apiUrl}/image-files`;

  constructor(private http: HttpClient) {
  }

  getImageFiles(dataset: string): Observable<ImageFile[]> {
    const queryUrl = `${this.imageFilesUrl}/${dataset}`
    return this.http.get<ImageFile[]>(queryUrl);
  }
}
