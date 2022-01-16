import {Injectable} from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {PredictionSettings} from "./prediction-settings";
import {Prediction} from "./prediction";

@Injectable({
  providedIn: 'root'
})
export class PredictionService {
  private predictionUrl = `${environment.apiUrl}/prediction`;

  constructor(private http: HttpClient) {
  }

  getPrediction(dataset: string, prediction: string, imageName: string, predictionSettings: PredictionSettings): Observable<Prediction> {
    const queryUrl = `${this.predictionUrl}/${dataset}/${prediction}/${imageName}`
    return this.http.get<Prediction>(queryUrl, {
      params: {
        stroke_size: predictionSettings.strokeSize,
        show_colored: predictionSettings.showColored,
        show_labeled: predictionSettings.showLabeled,
        font_size: predictionSettings.fontSize,
      }
    });
  }
}
