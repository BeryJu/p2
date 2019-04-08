import { Observable } from 'rxjs';
import { Blob } from '../api/models/blob';

export interface ExtraBlob extends Blob {

  pathName?: string;
  isPrefix?: boolean;
  prefixObject?: PathObject;

}

export class PathObject {

  name = '';
  children: Array<PathObject> = [];
  fullPrefix = '';

  expandable() {
    return this.children.length > 0;
  }

  hasChildren(name: string) {
    return this.children.map(child => child.name === name).length > 0;
  }

  getChild(name: string) {
    return this.children.filter(value => value.name === name)[0];
  }

}

export class PathHelper {

  public done: Observable<PathObject> = new Observable<PathObject>();

  private root: PathObject = new PathObject();

  constructor(private blobs: Array<Blob>) {
    this.root.name = 'Root';
    this.root.fullPrefix = '/';
  }

  build() {
    this.blobs.forEach(blob => {
      this.buildBlob(blob);
    });
    return this.root;
  }

  private buildBlob(blob: Blob) {
    const prefixParts = blob.path.split('/');
    // All parts start with a leading slash so we get "" at index 0
    prefixParts.shift();
    // We only want "folder" parts, so we remove the last part, which is the filename
    prefixParts.pop();
    // Check if anything is left, and if not, continue with the next
    if (prefixParts.length === 0) {
      return;
    }
    this.buildBlobParts(this.root, prefixParts);
  }

  private buildBlobParts(parent: PathObject, parts: Array<string>, path: string = '/') {
    const prefix = parts.shift();
    path += `${prefix}/`;
    let prefixObject = null;
    if (!parent.hasChildren(prefix)) {
      prefixObject = new PathObject();
      prefixObject.name = prefix;
      prefixObject.fullPrefix = path;
      parent.children.push(prefixObject);
    } else {
      prefixObject = parent.getChild(prefix);
    }
    if (parts.length > 0) {
      this.buildBlobParts(prefixObject, parts, path);
    }
  }

}
