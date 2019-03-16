import { Component, OnInit, Input, HostBinding } from '@angular/core';
import { DomSanitizer, SafeStyle } from '@angular/platform-browser';

@Component({
  selector: 'pyazo-image-tile',
  templateUrl: './image-tile.component.html',
  styleUrls: ['./image-tile.component.scss']
})
export class ImageTileComponent implements OnInit {

  @HostBinding('style.background') public background: SafeStyle;
  @Input() url: string;

  constructor(private domSanitizer: DomSanitizer) { }

  ngOnInit() {
    this.background = this.domSanitizer.bypassSecurityTrustStyle(
      `url("${this.url}") center top`
    );
  }

}
