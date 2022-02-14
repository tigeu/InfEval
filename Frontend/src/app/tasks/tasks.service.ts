import {Injectable} from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class TasksService {
  private tasksUrl = `${environment.apiUrl}/tasks`;

  constructor(private http: HttpClient) {
  }

  startTask(name: string, description: string, file_name: string, dataset_name: string, model_name: string): Observable<any> {
    console.log(name)
    const queryUrl = `${this.tasksUrl}/${name}`
    return this.http.post(queryUrl, {
      "task_description": description,
      "file_name": file_name,
      "dataset_name": dataset_name,
      "model_name": model_name
    });
  }
}
