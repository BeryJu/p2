import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

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

@NgModule({
  declarations: [
    AppComponent,
    FileBrowserComponent,
    ImageTileComponent,
    ImageViewComponent,
    PageGalleryComponent,
    SidebarComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ClarityModule,
    BrowserAnimationsModule,
    ApiModule,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
