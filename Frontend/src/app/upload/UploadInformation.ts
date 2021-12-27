import {UploadFileTypes} from "./UploadFileTypes";

export interface UploadInformation {
  uploadFileType: UploadFileTypes,
  uploadFileEnding: string,
  apiEndpoint: string
}
