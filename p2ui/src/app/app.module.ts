import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { ClarityModule } from '@clr/angular';
import { MatToolbarModule, MatButtonModule, MatIconModule } from '@angular/material';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';

import { AppComponent } from './app.component';
import { FileBrowserComponent } from './file-browser/file-browser.component';

import { ImageTileComponent } from './gallery/image-tile/image-tile.component';
import { ImageViewComponent } from './gallery/image-view/image-view.component';
import { PageGalleryComponent } from './gallery/page-gallery/page-gallery.component';
import { SidebarComponent } from './gallery/sidebar/sidebar.component';

import { ApiModule } from './api/api.module';
import { BlobViewComponent } from './blob/view/view.component';
import { BlobRendererBaseComponent } from './blob/renderer/base/base.component';
import { BlobRendererTextComponent } from './blob/renderer/text/text.component';
import { DynamicComponentService } from './utils/dynamic-component.service';
import { VolumeListComponent } from './volume/list/volume-list.component';
import { VolumeEditComponent } from './volume/edit/volume-edit.component';

@NgModule({
  declarations: [
    AppComponent,
    FileBrowserComponent,
    ImageTileComponent,
    ImageViewComponent,
    PageGalleryComponent,
    SidebarComponent,
    BlobViewComponent,
    BlobRendererTextComponent,
    BlobRendererBaseComponent,
    VolumeListComponent,
    VolumeEditComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ClarityModule,
    BrowserAnimationsModule,
    ApiModule,
    FormsModule,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
  ],
  providers: [
    DynamicComponentService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
