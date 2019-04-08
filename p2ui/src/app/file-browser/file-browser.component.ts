import { Component, OnInit } from '@angular/core';
import { Router } from "@angular/router";

import { CoreService } from '../api/services/core.service';
import { ClrDatagridStateInterface } from '@clr/angular';
import { PathHelper, PathObject, ExtraBlob } from '../utils/path';

@Component({
  selector: 'p2-file-browser',
  templateUrl: './file-browser.component.html',
  styleUrls: ['./file-browser.component.scss']
})
export class FileBrowserComponent implements OnInit {

  blobs: Blob[] = [];
  selected: Blob[] = [];

  prefixes: Array<PathObject> = [];
  total: number;
  loading = true;

  private currentPrefix: PathObject = new PathObject();
  private listParams: CoreService.CoreBlobListParams = {
    ordering: 'path',
    pathStartswith: '/'
  };

  constructor(
    private coreService: CoreService,
    private router: Router) { }

  ngOnInit() {
    this.update(true);
  }

  update(full: boolean = false) {
    this.loading = true;
    this.coreService.coreBlobList(this.listParams).subscribe(blobs => {
      if (full) {
        const pathHelper = new PathHelper(blobs.results);
        this.prefixes = [pathHelper.build()];
        this.currentPrefix = this.prefixes[0];
      }
      this.blobs = this.makeDatagridList(blobs.results);
      this.loading = false;
    });
  }

  makeDatagridList(blobs: Array<ExtraBlob>) {
    // debugger;
    // Remove currently selected fullPrefix from path of blob
    // add prefixes as `virtual` blobs to allow folder navigation
    const newBlobList = [];
    blobs.forEach(blob => {
      blob.pathName = blob.path.replace(this.listParams.pathStartswith, '');
      blob.isPrefix = false;
      // if blob still contains a / it's within another prefix, so we remove it
      if (blob.pathName.indexOf('/') === -1) {
        newBlobList.push(blob);
      }
    });
    this.currentPrefix.children.forEach(child => {
      newBlobList.push(<ExtraBlob>{
        path: child.name,
        pathName: child.name,
        attributes: {},
        isPrefix: true,
        prefixObject: child,
      });
    });
    return newBlobList;
  }

  getChildren(prefix: PathObject) {
    return prefix.children;
  }

  dblclickHandler(blob: ExtraBlob) {
    console.log("dblclick");
    if (blob.isPrefix) {
      this.changePrefix(blob.prefixObject);
    } else {
      this.router.navigate(['x/blob', blob.uuid ]);
    }
  }

  changePrefix(prefix: PathObject) {
    this.currentPrefix = prefix;
    this.listParams.pathStartswith = prefix.fullPrefix;
    console.log(`Changed prefix to ${prefix.fullPrefix}`);
    this.update();
  }

  refresh(state: ClrDatagridStateInterface) {
    this.loading = true;
    // We convert the filters from an array to a map,
    // because that's what our backend-calling service is expecting
    if (state.filters) {
      for (const filter of state.filters) {
        const { property, value } = <{ property: string, value: string }>filter;
        this.listParams[property] = [value];
      }
    }
    if (state.sort) {
      this.listParams.ordering = '';
      if (state.sort.reverse) {
        this.listParams.ordering = '-';
      }
      this.listParams.ordering += <string>state.sort.by;
    }
    this.update();
  }
}
