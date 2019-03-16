import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'pyazo-image-view',
  templateUrl: './image-view.component.html',
  styleUrls: ['./image-view.component.scss']
})
export class ImageViewComponent implements OnInit {

  url: string;

  constructor(private activatedRoute: ActivatedRoute) { }

  ngOnInit() {
    this.url = this.activatedRoute.snapshot.paramMap.get('id');
  }

}
