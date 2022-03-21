import {ClassMetricFile} from "./class-metric-file";

export interface PascalMetricFile {
  mAP: number;
  classes?: { className: ClassMetricFile };
  precision?: number;
  recall?: number;
  positives?: number;
  TP?: number;
  FP?: number;
}
