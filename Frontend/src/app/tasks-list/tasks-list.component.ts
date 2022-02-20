import {Component, OnInit} from '@angular/core';
import {TasksListService} from "./tasks-list.service";
import {interval, Subscription} from "rxjs";
import {TasksFile} from "./tasks-file";

@Component({
  selector: 'app-tasks-list',
  templateUrl: './tasks-list.component.html',
  styleUrls: ['./tasks-list.component.css']
})
export class TasksListComponent implements OnInit {

  tasksList: TasksFile[] = [];
  tasksListSubscription: Subscription = new Subscription;

  constructor(private tasksListService: TasksListService) {
    this.getTasksList();
  }

  ngOnInit(): void {
    this.tasksListSubscription = interval(5000)
      .subscribe(
        () => {
          this.getTasksList();
        }
      );
  }

  ngOnDestroy(): void {
    this.tasksListSubscription.unsubscribe();
  }

  getTasksList(): void {
    this.tasksListService.getTasksList()
      .subscribe((tasksList: TasksFile[]) => {
        this.tasksList = tasksList;
      })
  }
}
