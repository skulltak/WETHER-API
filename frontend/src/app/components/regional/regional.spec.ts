import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Regional } from './regional';

describe('Regional', () => {
  let component: Regional;
  let fixture: ComponentFixture<Regional>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Regional],
    }).compileComponents();

    fixture = TestBed.createComponent(Regional);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
