import {Injectable} from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from '@angular/common/http';
import {Heartbeat} from "./heartbeat";

@Injectable({
  providedIn: 'root'
})
export class HeartbeatService {
  private heartbeatUrl = 'http://localhost:8000/heartbeat';

  constructor(private http: HttpClient) {
  }

  getHeartbeat(heartbeat: Heartbeat): Observable<Heartbeat> {
    const url = `${this.heartbeatUrl}/${heartbeat.count}`
    return this.http.get<Heartbeat>(url);
  }
}
