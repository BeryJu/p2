import { ClrDatagridStateInterface } from '@clr/angular';
// import { ApiRequestConfiguration } from './auth';

export const camelize = function (str: String) {
  return str
    .replace(/_/g, ' ')
    .replace(/\s(.)/g, function ($1) { return $1.toUpperCase(); })
    .replace(/\s/g, '')
    .replace(/^(.)/, function ($1) { return $1.toLowerCase(); });
};

export interface Model {

  uuid?: string;

}

export interface ServiceListParams {
  /**
   * A search term.
   */
  search?: string;

  /**
   * Which field to use when ordering the results.
   */
  ordering?: string;

  /**
   * The initial index from which to return the results.
   */
  offset?: number;

  /**
   * Number of results to return per page.
   */
  limit?: number;
  hasCategory?: string;
}

export abstract class DatagridComponent<T1 extends Model, T2 extends ServiceListParams> {

  lastState: ClrDatagridStateInterface;
  loading = true;
  objects: Array<T1> = [];
  selected: Array<T1> = [];

  // constructor(private apiRequestConfiguration: ApiRequestConfiguration) {
  //   this.apiRequestConfiguration.userAuthenticationChange.subscribe(() => {
  //     this.refresh();
  //   });
  // }

  fetch(params: T2, done: () => any) { }

  bulkWrapper(func: (uuid: string, done: () => any) => any, done?: () => any) {
    this.loading = true;
    let __done = 0;
    this.selected.forEach(element => {
      func(element.uuid, () => {
        __done += 1;
        if (__done === this.selected.length) {
          this.loading = false;
          if (done) {
            done();
          }
          this.refresh();
        }
      });
    });
  }

  refresh(state?: ClrDatagridStateInterface) {
    if (state) {
      this.lastState = state;
    } else {
      state = this.lastState;
    }
    // State might be undefined as this could be an initial load
    // check for this and return early without load
    if (state === undefined) {
      return;
    }
    this.loading = true;
    const params = <T2>{};
    if (state.sort) {
      params.ordering = (state.sort.reverse ? '-' : '') + state.sort.by;
    }
    if (state.page) {
      params.limit = state.page.size;
      params.offset = state.page.from;
    }
    if (state.filters) {
      for (const filter of state.filters) {
        const { property, value } = <{ property: string, value: string }>filter;
        params[camelize(property) + 'Icontains'] = value;
      }
    }
    this.fetch(params, () => {
      setTimeout(() => {
        this.loading = false;
      }, 50);
    });
  }

}
