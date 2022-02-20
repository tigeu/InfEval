import {Injectable} from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {TasksFile} from "./tasks-file";

@Injectable({
  providedIn: 'root'
})
export class TasksListService {
  private tasksListUrl = `${environment.apiUrl}/tasks-list`;

  constructor(private http: HttpClient) {
  }

  getTasksList(): Observable<TasksFile[]> {
    return this.http.get<TasksFile[]>(this.tasksListUrl);
  }
}
