import { Component, OnDestroy, OnInit } from '@angular/core';
import { SensorService } from 'src/app/services/sensor.service';
import { Subject, timer, interval, forkJoin } from 'rxjs';
import { takeUntil, switchMap } from 'rxjs/operators';
import { HearbeatService } from 'src/app/services/hearbeat.service';

@Component({
  selector: 'app-vertical-bar',
  templateUrl: './vertical-bar.component.html',
  styleUrls: ['./vertical-bar.component.css']
})
export class VerticalBarComponent implements OnInit, OnDestroy {
  unsubscribe = new Subject();
  sensorIntervalTime = 3000;
  heartbeatIntervalTime = 1000;
  within = 10;
  data: any[];

  // options
  showXAxis = true;
  showYAxis = true;
  gradient = false;
  showLegend = true;
  showXAxisLabel = true;
  xAxisLabel = 'Sensors';
  showYAxisLabel = true;
  yAxisLabel = 'Users Detected';

  colorScheme = {
    domain: ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA']
  };

  heartbeatSet = new Set();
  offlineSensors = new Set();

  constructor(private sensorService: SensorService, private heartbeatService: HearbeatService) {
    this.data = [];
  }
  ngOnDestroy() {
    this.unsubscribe.next();
  }


  setupSensorData(sensors: any[]) {
    sensors.forEach(sensor => {
      if (!this.heartbeatSet.has(sensor.serial_number)) {
        this.heartbeatSet.add(sensor.serial_number);
        this.offlineSensors.add(sensor.serial_number);
      }
    })
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
      this.data = [...data];
      this.offlineSensors = downSensors;
    });
  }

  onSelect(event) {
    console.log(event);
  }

}
