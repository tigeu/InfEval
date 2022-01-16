import {Injectable} from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {GroundTruthSettings} from "./ground-truth-settings";
import {GroundTruth} from "./ground-truth";

@Injectable({
  providedIn: 'root'
})
export class GroundTruthService {
  private groundTruthUrl = `${environment.apiUrl}/ground-truth`;

  constructor(private http: HttpClient) {
  }

  getGroundTruth(dataset: string, imageName: string, groundTruthSettings: GroundTruthSettings): Observable<GroundTruth> {
    const queryUrl = `${this.groundTruthUrl}/${dataset}/${imageName}`
    return this.http.get<GroundTruth>(queryUrl, {
      params: {
        stroke_size: groundTruthSettings.strokeSize,
        show_colored: groundTruthSettings.showColored,
        show_labeled: groundTruthSettings.showLabeled,
        font_size: groundTruthSettings.fontSize,
      }
    });
  }
}
