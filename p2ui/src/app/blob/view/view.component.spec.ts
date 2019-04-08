import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BlobViewComponent } from './view.component';

describe('BlobViewComponent', () => {
  let component: BlobViewComponent;
  let fixture: ComponentFixture<BlobViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BlobViewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BlobViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
