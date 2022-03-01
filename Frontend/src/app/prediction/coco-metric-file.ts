import {ClassMetricFile} from "./class-metric-file";
import {CocoSummaryFile} from "./coco-summary-file";

export interface CocoMetricFile {
  summary?: CocoSummaryFile;
  classes?: { className: ClassMetricFile };
}
