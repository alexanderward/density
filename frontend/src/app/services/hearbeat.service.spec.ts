import { TestBed } from '@angular/core/testing';

import { HearbeatService } from './hearbeat.service';

describe('HearbeatService', () => {
  let service: HearbeatService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(HearbeatService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
