import {ClassMetricFile} from "./class-metric-file";

export interface PascalMetricFile {
  mAP: number;
  classes?: { className: ClassMetricFile };
}
