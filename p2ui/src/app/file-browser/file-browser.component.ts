import { Component, OnInit } from '@angular/core';

import { CoreService } from '../api/services/core.service';
import { Blob } from '../api/models/blob';
import { ClrDatagridStateInterface } from "@clr/angular";
import { PathHelper, PathObject } from '../utils/path';

@Component({
  selector: 'p2-file-browser',
  templateUrl: './file-browser.component.html',
  styleUrls: ['./file-browser.component.scss']
})
export class FileBrowserComponent implements OnInit {

  blobs: Blob[] = [];
  prefixes: PathObject = new PathObject();
  total: number;
  loading: boolean = true;

  constructor(private coreService: CoreService) { }

  ngOnInit() {
    this.coreService.coreBlobList(<CoreService.CoreBlobListParams>{}).subscribe(blobs => {
      this.blobs = blobs.results;
      let a = new PathHelper(blobs.results);
      this.prefixes = a.build();
      this.loading = false;
    });
  }

  getChildren (prefix: PathObject) {
    return prefix.children;
  }

  refresh(state: ClrDatagridStateInterface) {
    this.loading = true;
    // We convert the filters from an array to a map,
    // because that's what our backend-calling service is expecting
    let filters: { [prop: string]: any[] } = {};
    if (state.filters) {
      for (let filter of state.filters) {
        let { property, value } = <{ property: string, value: string }>filter;
        filters[property] = [value];
      }
    }
    // this.inventory.filter(filters)
    //   .sort(<{ by: string, reverse: boolean }>state.sort)
    //   .fetch(state.page.from, state.page.size)
    //   .then((result: FetchResult) => {
    //     this.users = result.users;
    //     this.total = result.length;
    //     this.loading = false;
    //   });
  }
}
