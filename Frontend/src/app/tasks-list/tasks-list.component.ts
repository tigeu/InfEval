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
  /*
  Component that gets a list of tasks from /tasks-list and displays them in a dropdown menu.

  Attributes
  ----------
  tasksListService : TasksListService
    Service for retrieving a list of predictions
  tasksList : TasksFile[]
    List of retrieved tasks
  tasksListSubscription : Subscription
    Subscription for updating tasks in interval

  Methods
  -------
  getTasksList(dataset: string)
    Calls service to retrieve the tasks list and save it to tasksList
  */
  tasksList: TasksFile[] = [];
  tasksListSubscription: Subscription = new Subscription;

  constructor(private tasksListService: TasksListService) {
    /*
    Retrieve list of tasks

    Parameters
    ----------
    tasksListService : TasksListService
      Service for retrieving a list of predictions
    */
    this.getTasksList();
  }

  ngOnInit(): void {
    /*
    Fetch updated task list every 5000ms
    */
    this.tasksListSubscription = interval(5000)
      .subscribe(
        () => {
          this.getTasksList();
        }
      );
  }

  ngOnDestroy(): void {
    /*
    Unsubscribe from all subscriptions
    */
    this.tasksListSubscription.unsubscribe();
  }

  getTasksList(): void {
    /*
    Calls service to retrieve the tasks list and save it to tasksList
    */
    this.tasksListService.getTasksList()
      .subscribe((tasksList: TasksFile[]) => {
        this.tasksList = tasksList;
      })
  }
}
