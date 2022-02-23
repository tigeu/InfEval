export interface PredictionSettings {
  showPrediction: boolean;
  strokeSize: number;
  showColored: boolean;
  showLabeled: boolean;
  fontSize: number;
  classes: string[];
  colors: string[];
  minConf: number;
  maxConf: number;
  iou: number;
  score: number;
}
