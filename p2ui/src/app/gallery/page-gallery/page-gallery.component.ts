import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'p2-page-gallery',
  templateUrl: './page-gallery.component.html',
  styleUrls: ['./page-gallery.component.scss']
})
export class PageGalleryComponent implements OnInit {

  urlList = [
  ];

  galleryId: string;

  constructor(private activatedRoute: ActivatedRoute) { }

  ngOnInit() {
    for (let index = 0; index < 50; index++) {
      this.urlList.push(`https://source.unsplash.com/random?${index}`);
    }
    this.galleryId = this.activatedRoute.snapshot.paramMap.get('id');
  }

}
