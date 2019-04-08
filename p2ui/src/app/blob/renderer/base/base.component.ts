import { Component, OnInit, Input } from '@angular/core';
import { Blob as MetaBlob } from '../../../api/models/blob';

@Component({
  selector: 'p2-base',
  templateUrl: './base.component.html',
  styleUrls: ['./base.component.scss']
})
export class BlobRendererBaseComponent implements OnInit {

  private _blob: Blob;
  private _metaBlob: MetaBlob;

  @Input()
  set blob (value: Blob) {
    this._blob = value;
    this.ngOnInit();
  }

  get blob () {
    return this._blob;
  }

  @Input()
  set metaBlob (value: MetaBlob) {
    this._metaBlob = value;
    this.ngOnInit();
  }

  get metaBlob () {
    return this._metaBlob;
  }

  constructor() { }

  ngOnInit() {
  }

}
