export interface OverviewTaskFile {
  name: string;
  description: string;
  progress: number;
  fileName: string;
  started: Date;
  finished: Date;
  dataset: string;
  model: string;
}
