import {Component, OnInit} from '@angular/core';
import {HttpClient, HttpEventType} from "@angular/common/http";
import {finalize, Subscription} from "rxjs";
import {environment} from "../../environments/environment";

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent implements OnInit {
  requiredFileType: String = "txt";
  private uploadUrl = `${environment.apiUrl}/upload`;

  fileName: String = '';
  uploadProgress!: number | null;
  uploadSub!: Subscription | null;

  constructor(private http: HttpClient) {
  }

  ngOnInit(): void {
  }

  onFileSelected(event: any) {
    const file: File = event.target.files[0];
    if (file) {
      this.fileName = file.name;
      const queryUrl = `${this.uploadUrl}/${this.fileName}`
      const formData = new FormData();
      formData.append("file", file);

      const upload = this.http.put(queryUrl, formData, {
        reportProgress: true,
        observe: 'events'
      }).pipe(
        finalize(() => this.reset())
      );

      this.uploadSub = upload.subscribe(event => {
        if (event.type == HttpEventType.UploadProgress) {
          console.log(event.total)
          if (event.total)
            this.uploadProgress = Math.round(100 * (event.loaded / event.total));
        }
      })
    }
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
