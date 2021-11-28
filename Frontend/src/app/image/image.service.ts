import {Injectable} from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from '@angular/common/http';
import {Image} from "./image";
import {environment} from "../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class ImageService {
  private imageUrl = `${environment.apiUrl}/image`;

  constructor(private http: HttpClient) {
  }

  getImage(imageName: String): Observable<Image> {
    const queryUrl = `${this.imageUrl}/${imageName}`
    return this.http.get<Image>(queryUrl);
  }
}
