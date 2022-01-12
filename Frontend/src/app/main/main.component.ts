import {Component, OnInit} from '@angular/core';
import {Heartbeat} from "./heartbeat";
import {interval, Subscription} from "rxjs";
import {HeartbeatService} from "./heartbeat.service";

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})

export class MainComponent implements OnInit {
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
          //this.getHeartbeat();
        }
      );
  }

  ngOnDestroy(): void {
    this.heartbeatSubscription.unsubscribe()
  }
}
