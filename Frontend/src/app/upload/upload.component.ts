import {Component, OnInit} from '@angular/core';
import {HttpEventType} from "@angular/common/http";
import {finalize, Subscription} from "rxjs";
import {UploadService} from "./upload.service";

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent implements OnInit {
  requiredFileType: String = ".zip";

  fileName: String = '';
  uploadProgress!: number | null;
  uploadSub!: Subscription | null;

  constructor(private uploadService: UploadService) {
  }

  ngOnInit(): void {
  }

  onFileSelected(event: any) {
    const file: File = event.target.files[0];
    if (!file)
      return

    this.fileName = file.name;

    this.uploadSub = this.uploadService.upload(this.fileName, file)
      .pipe(finalize(() => this.reset()))
      .subscribe(event => {
        if (event.type == HttpEventType.UploadProgress) {
          this.updateProgress(event.loaded, event.total);
        }
      })
  }

  updateProgress(loaded: number, total: number) {
    if (total)
      this.uploadProgress = Math.round(100 * (loaded / total));
  }

  cancelUpload() {
    if (this.uploadSub)
      this.uploadSub.unsubscribe();
    this.reset();
  }

  reset() {
    this.uploadProgress = null;
    this.uploadSub = null;
  }
}
