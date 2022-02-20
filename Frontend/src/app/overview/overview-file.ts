import {OverviewDatasetFile} from "./overview-dataset-file";
import {OverviewPredictionFile} from "./overview-prediction-file";
import {OverviewModelFile} from "./overview-model-file";
import {OverviewTaskFile} from "./overview-task-file";

export interface OverviewFile {
  datasets: OverviewDatasetFile[],
  predictions: OverviewPredictionFile[],
  models: OverviewModelFile[],
  tasks: OverviewTaskFile[]
}
