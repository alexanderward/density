import { Component, OnDestroy, OnInit } from '@angular/core';
import { SensorService } from 'src/app/services/sensor.service';
import { Subject, timer, interval, forkJoin } from 'rxjs';
import { takeUntil, switchMap } from 'rxjs/operators';
import { HearbeatService } from 'src/app/services/hearbeat.service';

@Component({
  selector: 'app-number-cards',
  templateUrl: './number-cards.component.html',
  styleUrls: ['./number-cards.component.css']
})
export class NumberCardsComponent implements OnInit, OnDestroy {
  unsubscribe = new Subject();
  sensorIntervalTime = 3000;
  heartbeatIntervalTime = 1000;
  within = 10;
  page = 1;
  pageSize = 4; 

  data: any[] = [];
  colorScheme = {
    domain: ['#5AA454', '#E44D25', '#CFC0BB', '#7aa3e5', '#a8385d', '#aae3f5']
  };
  cardColor: string = '#232837';

  heartbeatSet = new Set();
  offlineSensors = new Set();
  records = [];
  uniqueRecords = new Set();
  
  constructor(private sensorService: SensorService, private heartbeatService: HearbeatService) { }
  ngOnDestroy() {
    this.unsubscribe.next();
  }

  onSelect(event) {
    console.log(event);
  }

  setupSensorData(sensors: any[]) {
    sensors.forEach(sensor => {
      if (!this.heartbeatSet.has(sensor.serial_number)) {
        this.heartbeatSet.add(sensor.serial_number);
        this.offlineSensors.add(sensor.serial_number);
        this.data.push({
          "name": sensor.serial_number,
          "value": "0",
        });
      }
    });
    this.data = [...this.data];
  }

  buildHeartbeatCall() {
    let calls = []
    this.heartbeatSet.forEach((sensor: string) => {
      calls.push(this.heartbeatService.getHeartbeats(sensor, this.within))
    })
    return calls;
  }

  ngOnInit(): void {
    this.sensorService.getSensors().subscribe(data => {
      this.setupSensorData(data);
    })
    interval(this.sensorIntervalTime).pipe(
      takeUntil(this.unsubscribe),
      switchMap(() => this.sensorService.getSensors())
    ).subscribe(data => {
      this.setupSensorData(data);
    })

    interval(this.heartbeatIntervalTime).pipe(
      takeUntil(this.unsubscribe),
      switchMap(() => forkJoin(...this.buildHeartbeatCall()))
    ).subscribe((sensorBeats: any[]) => {
      let data = [];
      let downSensors = new Set(this.heartbeatSet);
      sensorBeats.forEach((beats: any[]) => {
        let count = 0;
        let serial_number;
        beats.forEach((beat: any) => {
          if (!this.uniqueRecords.has(`${beat.serial_number}-${beat.timestamp}`)) {
            this.records.push(beat);
            this.uniqueRecords.add(`${beat.serial_number}-${beat.timestamp}`);
            // todo - come up with a way to clear set to prevent memory overhead
          }
          ;
          count += beat.people_in_area;
          serial_number = beat.serial_number;
          if (beat.status === "DOWN") {
            downSensors.add(serial_number);
          } else {
            downSensors.delete(serial_number);
          }
        });
        if (serial_number !== undefined) {
          data.push({
            "name": serial_number,
            "value": `${count}`
          })
        }
      });
      data.forEach(x => {
        let found = this.data.find(item => item.name == x.name)
        if (found) {
          found.value = x.value;
        } else {
          this.data.push(x);
        }
      });
      this.data.forEach(obj => {
        if (downSensors.has(obj.name)) {
          obj.value = "0 - OFFLINE";
        }
      });
      this.data = [...this.data];
      this.offlineSensors = downSensors;
    });
  }
}
