export interface DatasetFile {
  name: string;
  ground_truth?: string;
  classes?: string[];
  colors?: string[];
  predictions?: boolean;
}
