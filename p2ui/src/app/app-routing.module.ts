import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { FileBrowserComponent } from './file-browser/file-browser.component';
import { BlobViewComponent } from './blob/view/view.component';
import { VolumeListComponent } from './volume/list/volume-list.component';

const routes: Routes = [
  { path: '', redirectTo: '/x/browser', pathMatch: 'full' },
  { path: 'x/browser', component: FileBrowserComponent },
  { path: 'x/volume', component: VolumeListComponent },
  { path: 'x/blob/:uuid', component: BlobViewComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
