import { Component, OnInit } from '@angular/core';
import { CoreService } from '../../api/services/core.service';
import { Volume } from '../../api/models/volume';
import { BaseStorage } from '../../api/models/base-storage';
import { DatagridComponent } from '../../utils/datagrid-base.component';

@Component({
  selector: 'p2-volume-list',
  templateUrl: './volume-list.component.html',
  styleUrls: ['./volume-list.component.scss']
})
export class VolumeListComponent extends DatagridComponent<Volume, CoreService.CoreVolumeListParams> {

  storages: { [key: string]: BaseStorage } = {};

  constructor(private coreService: CoreService) {
    super();
  }

  resolveStorage() {
    const storageList = [];
    this.objects.forEach(volume => {
      storageList.push(volume.storage);
    });
    const unique = Array.from(new Set(storageList));
    unique.forEach(storage => {
      this.coreService.coreStorageRead(storage).subscribe(response => {
        this.storages[storage] = response;
      });
    });
  }

  fetch(params: CoreService.CoreVolumeListParams, done: (total: number) => any) {
    this.coreService.coreVolumeList(params).subscribe(result => {
      this.objects = result.results;
      this.resolveStorage();
      done(result.count);
    });
  }

}
