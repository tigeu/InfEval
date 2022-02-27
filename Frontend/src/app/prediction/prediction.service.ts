import {Injectable} from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {PredictionSettings} from "./prediction-settings";
import {Prediction} from "./prediction";
import {PascalMetricFile} from "./pascal-metric-file";
import {CocoMetricFile} from "./coco-metric-file";

@Injectable({
  providedIn: 'root'
})
export class PredictionService {
  private predictionUrl = `${environment.apiUrl}/prediction`;
  private metricsUrl = `${environment.apiUrl}/metrics`;

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
        classes: predictionSettings.classes.join(','),
        colors: predictionSettings.colors.join(','),
        min_conf: predictionSettings.minConf,
        max_conf: predictionSettings.maxConf,
        nms_iou: predictionSettings.nmsIoU,
        nms_score: predictionSettings.nmsScore,
        only_ground_truth: predictionSettings.onlyGroundTruth,
        ground_truth_iou: predictionSettings.groundTruthIoU
      }
    });
  }

  getPascalMetric(dataset: string, prediction: string, imageName: string, predictionSettings: PredictionSettings): Observable<PascalMetricFile> {
    const queryUrl = `${this.metricsUrl}/${dataset}/${prediction}`
    return this.http.get<PascalMetricFile>(queryUrl, {
      params: {
        metric: "pascal",
        iou: 0.5,
        image_name: imageName,
        classes: predictionSettings.classes.join(','),
        min_conf: predictionSettings.minConf,
        max_conf: predictionSettings.maxConf,
        nms_iou: predictionSettings.nmsIoU,
        nms_score: predictionSettings.nmsScore,
      }
    });
  }

  getCocoMetric(dataset: string, prediction: string, imageName: string, predictionSettings: PredictionSettings): Observable<CocoMetricFile> {
    const queryUrl = `${this.metricsUrl}/${dataset}/${prediction}`
    return this.http.get<CocoMetricFile>(queryUrl, {
      params: {
        metric: predictionSettings.metric,
        iou: predictionSettings.IoU,
        image_name: imageName,
        classes: predictionSettings.classes.join(','),
        min_conf: predictionSettings.minConf,
        max_conf: predictionSettings.maxConf,
        nms_iou: predictionSettings.nmsIoU,
        nms_score: predictionSettings.nmsScore,
      }
    });
  }
}
