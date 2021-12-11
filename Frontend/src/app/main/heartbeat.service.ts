import {Injectable} from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from '@angular/common/http';
import {Heartbeat} from "./heartbeat";
import {environment} from "../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class HeartbeatService {
  private heartbeatUrl = `${environment.apiUrl}/heartbeat`;

  constructor(private http: HttpClient) {
  }

  getHeartbeat(heartbeat: Heartbeat): Observable<Heartbeat> {
    const url = `${this.heartbeatUrl}/${heartbeat.count}`
    return this.http.get<Heartbeat>(url);
  }
}
