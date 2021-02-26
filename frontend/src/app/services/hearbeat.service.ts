import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class HearbeatService {

  constructor(private httpClient: HttpClient) { }

  getHeartbeats(sensor: string, within: number) {
    const opts = { params: new HttpParams({fromString: `serial_number=${sensor}&within=${within}`}) };
    return this.httpClient.get<any[]>(`${environment.url}/heartbeats/`, opts);
  }
}
