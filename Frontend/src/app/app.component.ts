import {Component} from '@angular/core';
import {HeartbeatService} from "./heartbeat.service";
import {interval, Subscription} from "rxjs";
import {Heartbeat} from "./heartbeat";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  title = 'Object Detection Analyzer';

  heartbeat: Heartbeat = {count: 1};
  heartbeatSubscription: Subscription = new Subscription;

  constructor(private heartbeatService: HeartbeatService) {
  }

  getHeartbeat(): void {
    this.heartbeatService.getHeartbeat(this.heartbeat)
      .subscribe(heartbeat => this.heartbeat = heartbeat);
  }

  ngOnInit(): void {
    this.heartbeatSubscription = interval(5000)
      .subscribe(
        intervalResponse => {
          this.getHeartbeat();
        }
      );
  }
}
