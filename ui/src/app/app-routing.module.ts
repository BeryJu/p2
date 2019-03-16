import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { PageGalleryComponent } from './page-gallery/page-gallery.component';
import { ImageViewComponent } from './image-view/image-view.component';

const routes: Routes = [
  { path: '', component: PageGalleryComponent },
  { path: 'gallery/:id', component: PageGalleryComponent },
  { path: 'image/:id', component: ImageViewComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
