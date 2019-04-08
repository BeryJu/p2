import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { VolumeEditComponent } from './volume-edit.component';

describe('VolumeEditComponent', () => {
  let component: VolumeEditComponent;
  let fixture: ComponentFixture<VolumeEditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ VolumeEditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(VolumeEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
