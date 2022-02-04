import {UploadFileTypes} from "./UploadFileTypes";

export interface UploadInformation {
  isDataset: boolean,
  isModel: boolean,
  uploadFileType: UploadFileTypes,
  uploadFileEnding: string,
  apiEndpoint: string
}
