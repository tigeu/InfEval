import {UploadFileTypes} from "./UploadFileTypes";

export interface UploadInformation {
  isDataset: boolean,
  isModel: boolean,
  uploadFileTypes: UploadFileTypes[],
  uploadFileEnding: string,
  apiEndpoint: string
}
