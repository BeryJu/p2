import { Component, OnInit, Inject, ViewContainerRef } from '@angular/core';
import { ActivatedRoute } from "@angular/router";

import { CoreService } from '../../api/services/core.service';
import { Blob as MetaBlob } from '../../api/models/blob';
import { DynamicComponentService } from '../../utils/dynamic-component.service';

@Component({
  selector: 'p2-blob-view',
  templateUrl: './view.component.html',
  styleUrls: ['./view.component.scss']
})
export class BlobViewComponent implements OnInit {

  blob: MetaBlob = <MetaBlob>{};
  payload: Blob = new Blob();

  dynamicComponentService: DynamicComponentService;

  constructor(
      private coreService: CoreService,
      private route: ActivatedRoute,
      @Inject(DynamicComponentService) service,
      @Inject(ViewContainerRef) viewContainerRef) {
    this.dynamicComponentService = service;
    service.setRootViewContainerRef(viewContainerRef);
  }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const lookupParams = <CoreService.CoreBlobListParams>{
        uuid: params.get('uuid')
      };
      this.coreService.coreBlobList(lookupParams).subscribe(blob => {
        this.blob = blob.results[0];
        this.coreService.coreBlobPayload(this.blob.uuid).subscribe(response => {
          this.payload = this.b64toBlob(response.payload);
        });
      });
    });
  }

  b64toBlob(b64Data) {
    // convert base64 to raw binary data held in a string
    // doesn't handle URLEncoded DataURIs - see SO answer #6850276 for code that does this
    var byteString = atob(b64Data.split(',')[1]);

    // separate out the mime component
    var mimeString = b64Data.split(',')[0].split(':')[1].split(';')[0]

    // write the bytes of the string to an ArrayBuffer
    var ab = new ArrayBuffer(byteString.length);

    // create a view into the buffer
    var ia = new Uint8Array(ab);

    // set the bytes of the buffer to the correct values
    for (var i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
    }

    // write the ArrayBuffer to a blob, and you're done
    var blob = new Blob([ab], { type: mimeString });
    return blob;
  }


}
