import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SensorService {

  constructor(private httpClient: HttpClient) { }

  getSensors() {
    return this.httpClient.get<any[]>(`${environment.url}/sensors/`);
  }

  getSensor(sensor: string){
    const opts = { params: new HttpParams({fromString: `serial_number=${sensor}`}) };
    return this.httpClient.get<any>(`${environment.url}/sensors/`, opts);
  }
  
}

