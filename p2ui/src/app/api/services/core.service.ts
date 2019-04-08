/* tslint:disable */
import { Injectable } from '@angular/core';
import { HttpClient, HttpRequest, HttpResponse, HttpHeaders } from '@angular/common/http';
import { BaseService as __BaseService } from '../base-service';
import { ApiConfiguration as __Configuration } from '../api-configuration';
import { StrictHttpResponse as __StrictHttpResponse } from '../strict-http-response';
import { Observable as __Observable } from 'rxjs';
import { map as __map, filter as __filter } from 'rxjs/operators';

import { Blob } from '../models/blob';
import { BlobPayload } from '../models/blob-payload';
import { BaseStorage } from '../models/base-storage';
import { User } from '../models/user';
import { Volume } from '../models/volume';
@Injectable({
  providedIn: 'root',
})
class CoreService extends __BaseService {
  static readonly coreBlobListPath = '/core/blob/';
  static readonly coreBlobCreatePath = '/core/blob/';
  static readonly coreBlobReadPath = '/core/blob/{uuid}/';
  static readonly coreBlobUpdatePath = '/core/blob/{uuid}/';
  static readonly coreBlobPartialUpdatePath = '/core/blob/{uuid}/';
  static readonly coreBlobDeletePath = '/core/blob/{uuid}/';
  static readonly coreBlobPayloadPath = '/core/blob/{uuid}/payload/';
  static readonly coreStorageListPath = '/core/storage/';
  static readonly coreStorageCreatePath = '/core/storage/';
  static readonly coreStorageReadPath = '/core/storage/{uuid}/';
  static readonly coreStorageUpdatePath = '/core/storage/{uuid}/';
  static readonly coreStoragePartialUpdatePath = '/core/storage/{uuid}/';
  static readonly coreStorageDeletePath = '/core/storage/{uuid}/';
  static readonly coreUserListPath = '/core/user/';
  static readonly coreUserCreatePath = '/core/user/';
  static readonly coreUserReadPath = '/core/user/{id}/';
  static readonly coreUserUpdatePath = '/core/user/{id}/';
  static readonly coreUserPartialUpdatePath = '/core/user/{id}/';
  static readonly coreUserDeletePath = '/core/user/{id}/';
  static readonly coreVolumeListPath = '/core/volume/';
  static readonly coreVolumeCreatePath = '/core/volume/';
  static readonly coreVolumeReadPath = '/core/volume/{uuid}/';
  static readonly coreVolumeUpdatePath = '/core/volume/{uuid}/';
  static readonly coreVolumePartialUpdatePath = '/core/volume/{uuid}/';
  static readonly coreVolumeDeletePath = '/core/volume/{uuid}/';

  constructor(
    config: __Configuration,
    http: HttpClient
  ) {
    super(config, http);
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreBlobListParams` containing the following parameters:
   *
   * - `volume`:
   *
   * - `uuid__icontains`:
   *
   * - `uuid`:
   *
   * - `search`: A search term.
   *
   * - `path__startswith`:
   *
   * - `path__icontains`:
   *
   * - `path`:
   *
   * - `ordering`: Which field to use when ordering the results.
   *
   * - `offset`: The initial index from which to return the results.
   *
   * - `limit`: Number of results to return per page.
   */
  coreBlobListResponse(params: CoreService.CoreBlobListParams): __Observable<__StrictHttpResponse<{count: number, next?: null | string, previous?: null | string, results: Array<Blob>}>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;
    if (params.volume != null) __params = __params.set('volume', params.volume.toString());
    if (params.uuidIcontains != null) __params = __params.set('uuid__icontains', params.uuidIcontains.toString());
    if (params.uuid != null) __params = __params.set('uuid', params.uuid.toString());
    if (params.search != null) __params = __params.set('search', params.search.toString());
    if (params.pathStartswith != null) __params = __params.set('path__startswith', params.pathStartswith.toString());
    if (params.pathIcontains != null) __params = __params.set('path__icontains', params.pathIcontains.toString());
    if (params.path != null) __params = __params.set('path', params.path.toString());
    if (params.ordering != null) __params = __params.set('ordering', params.ordering.toString());
    if (params.offset != null) __params = __params.set('offset', params.offset.toString());
    if (params.limit != null) __params = __params.set('limit', params.limit.toString());
    let req = new HttpRequest<any>(
      'GET',
      this.rootUrl + `/core/blob/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<{count: number, next?: null | string, previous?: null | string, results: Array<Blob>}>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreBlobListParams` containing the following parameters:
   *
   * - `volume`:
   *
   * - `uuid__icontains`:
   *
   * - `uuid`:
   *
   * - `search`: A search term.
   *
   * - `path__startswith`:
   *
   * - `path__icontains`:
   *
   * - `path`:
   *
   * - `ordering`: Which field to use when ordering the results.
   *
   * - `offset`: The initial index from which to return the results.
   *
   * - `limit`: Number of results to return per page.
   */
  coreBlobList(params: CoreService.CoreBlobListParams): __Observable<{count: number, next?: null | string, previous?: null | string, results: Array<Blob>}> {
    return this.coreBlobListResponse(params).pipe(
      __map(_r => _r.body as {count: number, next?: null | string, previous?: null | string, results: Array<Blob>})
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param data undefined
   */
  coreBlobCreateResponse(data: Blob): __Observable<__StrictHttpResponse<Blob>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;
    __body = data;
    let req = new HttpRequest<any>(
      'POST',
      this.rootUrl + `/core/blob/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'blob'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<Blob>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param data undefined
   */
  coreBlobCreate(data: Blob): __Observable<Blob> {
    return this.coreBlobCreateResponse(data).pipe(
      __map(_r => _r.body as Blob)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param uuid A UUID string identifying this blob.
   */
  coreBlobReadResponse(uuid: string): __Observable<__StrictHttpResponse<Blob>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    let req = new HttpRequest<any>(
      'GET',
      this.rootUrl + `/core/blob/${uuid}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'blob'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<Blob>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param uuid A UUID string identifying this blob.
   */
  coreBlobRead(uuid: string): __Observable<Blob> {
    return this.coreBlobReadResponse(uuid).pipe(
      __map(_r => _r.body as Blob)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreBlobUpdateParams` containing the following parameters:
   *
   * - `uuid`: A UUID string identifying this blob.
   *
   * - `data`:
   */
  coreBlobUpdateResponse(params: CoreService.CoreBlobUpdateParams): __Observable<__StrictHttpResponse<Blob>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    __body = params.data;
    let req = new HttpRequest<any>(
      'PUT',
      this.rootUrl + `/core/blob/${params.uuid}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'blob'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<Blob>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreBlobUpdateParams` containing the following parameters:
   *
   * - `uuid`: A UUID string identifying this blob.
   *
   * - `data`:
   */
  coreBlobUpdate(params: CoreService.CoreBlobUpdateParams): __Observable<Blob> {
    return this.coreBlobUpdateResponse(params).pipe(
      __map(_r => _r.body as Blob)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreBlobPartialUpdateParams` containing the following parameters:
   *
   * - `uuid`: A UUID string identifying this blob.
   *
   * - `data`:
   */
  coreBlobPartialUpdateResponse(params: CoreService.CoreBlobPartialUpdateParams): __Observable<__StrictHttpResponse<Blob>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    __body = params.data;
    let req = new HttpRequest<any>(
      'PATCH',
      this.rootUrl + `/core/blob/${params.uuid}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'blob'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<Blob>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreBlobPartialUpdateParams` containing the following parameters:
   *
   * - `uuid`: A UUID string identifying this blob.
   *
   * - `data`:
   */
  coreBlobPartialUpdate(params: CoreService.CoreBlobPartialUpdateParams): __Observable<Blob> {
    return this.coreBlobPartialUpdateResponse(params).pipe(
      __map(_r => _r.body as Blob)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param uuid A UUID string identifying this blob.
   */
  coreBlobDeleteResponse(uuid: string): __Observable<__StrictHttpResponse<null>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    let req = new HttpRequest<any>(
      'DELETE',
      this.rootUrl + `/core/blob/${uuid}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<null>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param uuid A UUID string identifying this blob.
   */
  coreBlobDelete(uuid: string): __Observable<null> {
    return this.coreBlobDeleteResponse(uuid).pipe(
      __map(_r => _r.body as null)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param uuid A UUID string identifying this blob.
   */
  coreBlobPayloadResponse(uuid: string): __Observable<__StrictHttpResponse<BlobPayload>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    let req = new HttpRequest<any>(
      'GET',
      this.rootUrl + `/core/blob/${uuid}/payload/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<BlobPayload>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param uuid A UUID string identifying this blob.
   */
  coreBlobPayload(uuid: string): __Observable<BlobPayload> {
    return this.coreBlobPayloadResponse(uuid).pipe(
      __map(_r => _r.body as BlobPayload)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreStorageListParams` containing the following parameters:
   *
   * - `search`: A search term.
   *
   * - `ordering`: Which field to use when ordering the results.
   *
   * - `offset`: The initial index from which to return the results.
   *
   * - `limit`: Number of results to return per page.
   */
  coreStorageListResponse(params: CoreService.CoreStorageListParams): __Observable<__StrictHttpResponse<{count: number, next?: null | string, previous?: null | string, results: Array<BaseStorage>}>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;
    if (params.search != null) __params = __params.set('search', params.search.toString());
    if (params.ordering != null) __params = __params.set('ordering', params.ordering.toString());
    if (params.offset != null) __params = __params.set('offset', params.offset.toString());
    if (params.limit != null) __params = __params.set('limit', params.limit.toString());
    let req = new HttpRequest<any>(
      'GET',
      this.rootUrl + `/core/storage/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<{count: number, next?: null | string, previous?: null | string, results: Array<BaseStorage>}>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreStorageListParams` containing the following parameters:
   *
   * - `search`: A search term.
   *
   * - `ordering`: Which field to use when ordering the results.
   *
   * - `offset`: The initial index from which to return the results.
   *
   * - `limit`: Number of results to return per page.
   */
  coreStorageList(params: CoreService.CoreStorageListParams): __Observable<{count: number, next?: null | string, previous?: null | string, results: Array<BaseStorage>}> {
    return this.coreStorageListResponse(params).pipe(
      __map(_r => _r.body as {count: number, next?: null | string, previous?: null | string, results: Array<BaseStorage>})
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param data undefined
   */
  coreStorageCreateResponse(data: BaseStorage): __Observable<__StrictHttpResponse<BaseStorage>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;
    __body = data;
    let req = new HttpRequest<any>(
      'POST',
      this.rootUrl + `/core/storage/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<BaseStorage>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param data undefined
   */
  coreStorageCreate(data: BaseStorage): __Observable<BaseStorage> {
    return this.coreStorageCreateResponse(data).pipe(
      __map(_r => _r.body as BaseStorage)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param uuid A UUID string identifying this base storage.
   */
  coreStorageReadResponse(uuid: string): __Observable<__StrictHttpResponse<BaseStorage>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    let req = new HttpRequest<any>(
      'GET',
      this.rootUrl + `/core/storage/${uuid}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<BaseStorage>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param uuid A UUID string identifying this base storage.
   */
  coreStorageRead(uuid: string): __Observable<BaseStorage> {
    return this.coreStorageReadResponse(uuid).pipe(
      __map(_r => _r.body as BaseStorage)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreStorageUpdateParams` containing the following parameters:
   *
   * - `uuid`: A UUID string identifying this base storage.
   *
   * - `data`:
   */
  coreStorageUpdateResponse(params: CoreService.CoreStorageUpdateParams): __Observable<__StrictHttpResponse<BaseStorage>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    __body = params.data;
    let req = new HttpRequest<any>(
      'PUT',
      this.rootUrl + `/core/storage/${params.uuid}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<BaseStorage>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreStorageUpdateParams` containing the following parameters:
   *
   * - `uuid`: A UUID string identifying this base storage.
   *
   * - `data`:
   */
  coreStorageUpdate(params: CoreService.CoreStorageUpdateParams): __Observable<BaseStorage> {
    return this.coreStorageUpdateResponse(params).pipe(
      __map(_r => _r.body as BaseStorage)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreStoragePartialUpdateParams` containing the following parameters:
   *
   * - `uuid`: A UUID string identifying this base storage.
   *
   * - `data`:
   */
  coreStoragePartialUpdateResponse(params: CoreService.CoreStoragePartialUpdateParams): __Observable<__StrictHttpResponse<BaseStorage>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    __body = params.data;
    let req = new HttpRequest<any>(
      'PATCH',
      this.rootUrl + `/core/storage/${params.uuid}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<BaseStorage>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreStoragePartialUpdateParams` containing the following parameters:
   *
   * - `uuid`: A UUID string identifying this base storage.
   *
   * - `data`:
   */
  coreStoragePartialUpdate(params: CoreService.CoreStoragePartialUpdateParams): __Observable<BaseStorage> {
    return this.coreStoragePartialUpdateResponse(params).pipe(
      __map(_r => _r.body as BaseStorage)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param uuid A UUID string identifying this base storage.
   */
  coreStorageDeleteResponse(uuid: string): __Observable<__StrictHttpResponse<null>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    let req = new HttpRequest<any>(
      'DELETE',
      this.rootUrl + `/core/storage/${uuid}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<null>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param uuid A UUID string identifying this base storage.
   */
  coreStorageDelete(uuid: string): __Observable<null> {
    return this.coreStorageDeleteResponse(uuid).pipe(
      __map(_r => _r.body as null)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreUserListParams` containing the following parameters:
   *
   * - `search`: A search term.
   *
   * - `ordering`: Which field to use when ordering the results.
   *
   * - `offset`: The initial index from which to return the results.
   *
   * - `limit`: Number of results to return per page.
   */
  coreUserListResponse(params: CoreService.CoreUserListParams): __Observable<__StrictHttpResponse<{count: number, next?: null | string, previous?: null | string, results: Array<User>}>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;
    if (params.search != null) __params = __params.set('search', params.search.toString());
    if (params.ordering != null) __params = __params.set('ordering', params.ordering.toString());
    if (params.offset != null) __params = __params.set('offset', params.offset.toString());
    if (params.limit != null) __params = __params.set('limit', params.limit.toString());
    let req = new HttpRequest<any>(
      'GET',
      this.rootUrl + `/core/user/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<{count: number, next?: null | string, previous?: null | string, results: Array<User>}>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreUserListParams` containing the following parameters:
   *
   * - `search`: A search term.
   *
   * - `ordering`: Which field to use when ordering the results.
   *
   * - `offset`: The initial index from which to return the results.
   *
   * - `limit`: Number of results to return per page.
   */
  coreUserList(params: CoreService.CoreUserListParams): __Observable<{count: number, next?: null | string, previous?: null | string, results: Array<User>}> {
    return this.coreUserListResponse(params).pipe(
      __map(_r => _r.body as {count: number, next?: null | string, previous?: null | string, results: Array<User>})
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param data undefined
   */
  coreUserCreateResponse(data: User): __Observable<__StrictHttpResponse<User>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;
    __body = data;
    let req = new HttpRequest<any>(
      'POST',
      this.rootUrl + `/core/user/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<User>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param data undefined
   */
  coreUserCreate(data: User): __Observable<User> {
    return this.coreUserCreateResponse(data).pipe(
      __map(_r => _r.body as User)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param id A unique integer value identifying this user.
   */
  coreUserReadResponse(id: number): __Observable<__StrictHttpResponse<User>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    let req = new HttpRequest<any>(
      'GET',
      this.rootUrl + `/core/user/${id}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<User>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param id A unique integer value identifying this user.
   */
  coreUserRead(id: number): __Observable<User> {
    return this.coreUserReadResponse(id).pipe(
      __map(_r => _r.body as User)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreUserUpdateParams` containing the following parameters:
   *
   * - `id`: A unique integer value identifying this user.
   *
   * - `data`:
   */
  coreUserUpdateResponse(params: CoreService.CoreUserUpdateParams): __Observable<__StrictHttpResponse<User>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    __body = params.data;
    let req = new HttpRequest<any>(
      'PUT',
      this.rootUrl + `/core/user/${params.id}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<User>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreUserUpdateParams` containing the following parameters:
   *
   * - `id`: A unique integer value identifying this user.
   *
   * - `data`:
   */
  coreUserUpdate(params: CoreService.CoreUserUpdateParams): __Observable<User> {
    return this.coreUserUpdateResponse(params).pipe(
      __map(_r => _r.body as User)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreUserPartialUpdateParams` containing the following parameters:
   *
   * - `id`: A unique integer value identifying this user.
   *
   * - `data`:
   */
  coreUserPartialUpdateResponse(params: CoreService.CoreUserPartialUpdateParams): __Observable<__StrictHttpResponse<User>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    __body = params.data;
    let req = new HttpRequest<any>(
      'PATCH',
      this.rootUrl + `/core/user/${params.id}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<User>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreUserPartialUpdateParams` containing the following parameters:
   *
   * - `id`: A unique integer value identifying this user.
   *
   * - `data`:
   */
  coreUserPartialUpdate(params: CoreService.CoreUserPartialUpdateParams): __Observable<User> {
    return this.coreUserPartialUpdateResponse(params).pipe(
      __map(_r => _r.body as User)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param id A unique integer value identifying this user.
   */
  coreUserDeleteResponse(id: number): __Observable<__StrictHttpResponse<null>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    let req = new HttpRequest<any>(
      'DELETE',
      this.rootUrl + `/core/user/${id}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<null>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param id A unique integer value identifying this user.
   */
  coreUserDelete(id: number): __Observable<null> {
    return this.coreUserDeleteResponse(id).pipe(
      __map(_r => _r.body as null)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreVolumeListParams` containing the following parameters:
   *
   * - `search`: A search term.
   *
   * - `ordering`: Which field to use when ordering the results.
   *
   * - `offset`: The initial index from which to return the results.
   *
   * - `limit`: Number of results to return per page.
   */
  coreVolumeListResponse(params: CoreService.CoreVolumeListParams): __Observable<__StrictHttpResponse<{count: number, next?: null | string, previous?: null | string, results: Array<Volume>}>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;
    if (params.search != null) __params = __params.set('search', params.search.toString());
    if (params.ordering != null) __params = __params.set('ordering', params.ordering.toString());
    if (params.offset != null) __params = __params.set('offset', params.offset.toString());
    if (params.limit != null) __params = __params.set('limit', params.limit.toString());
    let req = new HttpRequest<any>(
      'GET',
      this.rootUrl + `/core/volume/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<{count: number, next?: null | string, previous?: null | string, results: Array<Volume>}>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreVolumeListParams` containing the following parameters:
   *
   * - `search`: A search term.
   *
   * - `ordering`: Which field to use when ordering the results.
   *
   * - `offset`: The initial index from which to return the results.
   *
   * - `limit`: Number of results to return per page.
   */
  coreVolumeList(params: CoreService.CoreVolumeListParams): __Observable<{count: number, next?: null | string, previous?: null | string, results: Array<Volume>}> {
    return this.coreVolumeListResponse(params).pipe(
      __map(_r => _r.body as {count: number, next?: null | string, previous?: null | string, results: Array<Volume>})
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param data undefined
   */
  coreVolumeCreateResponse(data: Volume): __Observable<__StrictHttpResponse<Volume>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;
    __body = data;
    let req = new HttpRequest<any>(
      'POST',
      this.rootUrl + `/core/volume/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<Volume>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param data undefined
   */
  coreVolumeCreate(data: Volume): __Observable<Volume> {
    return this.coreVolumeCreateResponse(data).pipe(
      __map(_r => _r.body as Volume)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param uuid A UUID string identifying this volume.
   */
  coreVolumeReadResponse(uuid: string): __Observable<__StrictHttpResponse<Volume>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    let req = new HttpRequest<any>(
      'GET',
      this.rootUrl + `/core/volume/${uuid}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<Volume>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param uuid A UUID string identifying this volume.
   */
  coreVolumeRead(uuid: string): __Observable<Volume> {
    return this.coreVolumeReadResponse(uuid).pipe(
      __map(_r => _r.body as Volume)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreVolumeUpdateParams` containing the following parameters:
   *
   * - `uuid`: A UUID string identifying this volume.
   *
   * - `data`:
   */
  coreVolumeUpdateResponse(params: CoreService.CoreVolumeUpdateParams): __Observable<__StrictHttpResponse<Volume>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    __body = params.data;
    let req = new HttpRequest<any>(
      'PUT',
      this.rootUrl + `/core/volume/${params.uuid}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<Volume>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreVolumeUpdateParams` containing the following parameters:
   *
   * - `uuid`: A UUID string identifying this volume.
   *
   * - `data`:
   */
  coreVolumeUpdate(params: CoreService.CoreVolumeUpdateParams): __Observable<Volume> {
    return this.coreVolumeUpdateResponse(params).pipe(
      __map(_r => _r.body as Volume)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreVolumePartialUpdateParams` containing the following parameters:
   *
   * - `uuid`: A UUID string identifying this volume.
   *
   * - `data`:
   */
  coreVolumePartialUpdateResponse(params: CoreService.CoreVolumePartialUpdateParams): __Observable<__StrictHttpResponse<Volume>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    __body = params.data;
    let req = new HttpRequest<any>(
      'PATCH',
      this.rootUrl + `/core/volume/${params.uuid}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<Volume>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `CoreService.CoreVolumePartialUpdateParams` containing the following parameters:
   *
   * - `uuid`: A UUID string identifying this volume.
   *
   * - `data`:
   */
  coreVolumePartialUpdate(params: CoreService.CoreVolumePartialUpdateParams): __Observable<Volume> {
    return this.coreVolumePartialUpdateResponse(params).pipe(
      __map(_r => _r.body as Volume)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param uuid A UUID string identifying this volume.
   */
  coreVolumeDeleteResponse(uuid: string): __Observable<__StrictHttpResponse<null>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    let req = new HttpRequest<any>(
      'DELETE',
      this.rootUrl + `/core/volume/${uuid}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<null>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param uuid A UUID string identifying this volume.
   */
  coreVolumeDelete(uuid: string): __Observable<null> {
    return this.coreVolumeDeleteResponse(uuid).pipe(
      __map(_r => _r.body as null)
    );
  }
}

module CoreService {

  /**
   * Parameters for coreBlobList
   */
  export interface CoreBlobListParams {
    volume?: string;
    uuidIcontains?: string;
    uuid?: string;

    /**
     * A search term.
     */
    search?: string;
    pathStartswith?: string;
    pathIcontains?: string;
    path?: string;

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
  }

  /**
   * Parameters for coreBlobUpdate
   */
  export interface CoreBlobUpdateParams {

    /**
     * A UUID string identifying this blob.
     */
    uuid: string;
    data: Blob;
  }

  /**
   * Parameters for coreBlobPartialUpdate
   */
  export interface CoreBlobPartialUpdateParams {

    /**
     * A UUID string identifying this blob.
     */
    uuid: string;
    data: Blob;
  }

  /**
   * Parameters for coreStorageList
   */
  export interface CoreStorageListParams {

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
  }

  /**
   * Parameters for coreStorageUpdate
   */
  export interface CoreStorageUpdateParams {

    /**
     * A UUID string identifying this base storage.
     */
    uuid: string;
    data: BaseStorage;
  }

  /**
   * Parameters for coreStoragePartialUpdate
   */
  export interface CoreStoragePartialUpdateParams {

    /**
     * A UUID string identifying this base storage.
     */
    uuid: string;
    data: BaseStorage;
  }

  /**
   * Parameters for coreUserList
   */
  export interface CoreUserListParams {

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
  }

  /**
   * Parameters for coreUserUpdate
   */
  export interface CoreUserUpdateParams {

    /**
     * A unique integer value identifying this user.
     */
    id: number;
    data: User;
  }

  /**
   * Parameters for coreUserPartialUpdate
   */
  export interface CoreUserPartialUpdateParams {

    /**
     * A unique integer value identifying this user.
     */
    id: number;
    data: User;
  }

  /**
   * Parameters for coreVolumeList
   */
  export interface CoreVolumeListParams {

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
  }

  /**
   * Parameters for coreVolumeUpdate
   */
  export interface CoreVolumeUpdateParams {

    /**
     * A UUID string identifying this volume.
     */
    uuid: string;
    data: Volume;
  }

  /**
   * Parameters for coreVolumePartialUpdate
   */
  export interface CoreVolumePartialUpdateParams {

    /**
     * A UUID string identifying this volume.
     */
    uuid: string;
    data: Volume;
  }
}

export { CoreService }
