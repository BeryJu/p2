import { Component, OnInit } from '@angular/core';
import { BlobRendererBaseComponent } from '../base/base.component';

@Component({
  selector: 'p2-text',
  templateUrl: './text.component.html',
  styleUrls: ['./text.component.scss']
})
export class BlobRendererTextComponent extends BlobRendererBaseComponent implements OnInit {

  text: string;

  constructor() {
    super();
  }

  async ngOnInit() {
    this.text = await(new Response(this.blob)).text();
  }

}
