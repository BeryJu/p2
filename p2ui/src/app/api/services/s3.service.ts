/* tslint:disable */
import { Injectable } from '@angular/core';
import { HttpClient, HttpRequest, HttpResponse, HttpHeaders } from '@angular/common/http';
import { BaseService as __BaseService } from '../base-service';
import { ApiConfiguration as __Configuration } from '../api-configuration';
import { StrictHttpResponse as __StrictHttpResponse } from '../strict-http-response';
import { Observable as __Observable } from 'rxjs';
import { map as __map, filter as __filter } from 'rxjs/operators';

import { S3AccessKey } from '../models/s3access-key';
@Injectable({
  providedIn: 'root',
})
class S3Service extends __BaseService {
  static readonly s3AccessKeyListPath = '/s3/access_key/';
  static readonly s3AccessKeyCreatePath = '/s3/access_key/';
  static readonly s3AccessKeyReadPath = '/s3/access_key/{id}/';
  static readonly s3AccessKeyUpdatePath = '/s3/access_key/{id}/';
  static readonly s3AccessKeyPartialUpdatePath = '/s3/access_key/{id}/';
  static readonly s3AccessKeyDeletePath = '/s3/access_key/{id}/';

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
   * @param params The `S3Service.S3AccessKeyListParams` containing the following parameters:
   *
   * - `offset`: The initial index from which to return the results.
   *
   * - `limit`: Number of results to return per page.
   */
  s3AccessKeyListResponse(params: S3Service.S3AccessKeyListParams): __Observable<__StrictHttpResponse<{count: number, next?: null | string, previous?: null | string, results: Array<S3AccessKey>}>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;
    if (params.offset != null) __params = __params.set('offset', params.offset.toString());
    if (params.limit != null) __params = __params.set('limit', params.limit.toString());
    let req = new HttpRequest<any>(
      'GET',
      this.rootUrl + `/s3/access_key/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<{count: number, next?: null | string, previous?: null | string, results: Array<S3AccessKey>}>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `S3Service.S3AccessKeyListParams` containing the following parameters:
   *
   * - `offset`: The initial index from which to return the results.
   *
   * - `limit`: Number of results to return per page.
   */
  s3AccessKeyList(params: S3Service.S3AccessKeyListParams): __Observable<{count: number, next?: null | string, previous?: null | string, results: Array<S3AccessKey>}> {
    return this.s3AccessKeyListResponse(params).pipe(
      __map(_r => _r.body as {count: number, next?: null | string, previous?: null | string, results: Array<S3AccessKey>})
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param data undefined
   */
  s3AccessKeyCreateResponse(data: S3AccessKey): __Observable<__StrictHttpResponse<S3AccessKey>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;
    __body = data;
    let req = new HttpRequest<any>(
      'POST',
      this.rootUrl + `/s3/access_key/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<S3AccessKey>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param data undefined
   */
  s3AccessKeyCreate(data: S3AccessKey): __Observable<S3AccessKey> {
    return this.s3AccessKeyCreateResponse(data).pipe(
      __map(_r => _r.body as S3AccessKey)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param id A unique integer value identifying this S3 Access Key.
   */
  s3AccessKeyReadResponse(id: number): __Observable<__StrictHttpResponse<S3AccessKey>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    let req = new HttpRequest<any>(
      'GET',
      this.rootUrl + `/s3/access_key/${id}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<S3AccessKey>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param id A unique integer value identifying this S3 Access Key.
   */
  s3AccessKeyRead(id: number): __Observable<S3AccessKey> {
    return this.s3AccessKeyReadResponse(id).pipe(
      __map(_r => _r.body as S3AccessKey)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `S3Service.S3AccessKeyUpdateParams` containing the following parameters:
   *
   * - `id`: A unique integer value identifying this S3 Access Key.
   *
   * - `data`:
   */
  s3AccessKeyUpdateResponse(params: S3Service.S3AccessKeyUpdateParams): __Observable<__StrictHttpResponse<S3AccessKey>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    __body = params.data;
    let req = new HttpRequest<any>(
      'PUT',
      this.rootUrl + `/s3/access_key/${params.id}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<S3AccessKey>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `S3Service.S3AccessKeyUpdateParams` containing the following parameters:
   *
   * - `id`: A unique integer value identifying this S3 Access Key.
   *
   * - `data`:
   */
  s3AccessKeyUpdate(params: S3Service.S3AccessKeyUpdateParams): __Observable<S3AccessKey> {
    return this.s3AccessKeyUpdateResponse(params).pipe(
      __map(_r => _r.body as S3AccessKey)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `S3Service.S3AccessKeyPartialUpdateParams` containing the following parameters:
   *
   * - `id`: A unique integer value identifying this S3 Access Key.
   *
   * - `data`:
   */
  s3AccessKeyPartialUpdateResponse(params: S3Service.S3AccessKeyPartialUpdateParams): __Observable<__StrictHttpResponse<S3AccessKey>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    __body = params.data;
    let req = new HttpRequest<any>(
      'PATCH',
      this.rootUrl + `/s3/access_key/${params.id}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<S3AccessKey>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `S3Service.S3AccessKeyPartialUpdateParams` containing the following parameters:
   *
   * - `id`: A unique integer value identifying this S3 Access Key.
   *
   * - `data`:
   */
  s3AccessKeyPartialUpdate(params: S3Service.S3AccessKeyPartialUpdateParams): __Observable<S3AccessKey> {
    return this.s3AccessKeyPartialUpdateResponse(params).pipe(
      __map(_r => _r.body as S3AccessKey)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param id A unique integer value identifying this S3 Access Key.
   */
  s3AccessKeyDeleteResponse(id: number): __Observable<__StrictHttpResponse<null>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    let req = new HttpRequest<any>(
      'DELETE',
      this.rootUrl + `/s3/access_key/${id}/`,
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
   * @param id A unique integer value identifying this S3 Access Key.
   */
  s3AccessKeyDelete(id: number): __Observable<null> {
    return this.s3AccessKeyDeleteResponse(id).pipe(
      __map(_r => _r.body as null)
    );
  }
}

module S3Service {

  /**
   * Parameters for s3AccessKeyList
   */
  export interface S3AccessKeyListParams {

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
   * Parameters for s3AccessKeyUpdate
   */
  export interface S3AccessKeyUpdateParams {

    /**
     * A unique integer value identifying this S3 Access Key.
     */
    id: number;
    data: S3AccessKey;
  }

  /**
   * Parameters for s3AccessKeyPartialUpdate
   */
  export interface S3AccessKeyPartialUpdateParams {

    /**
     * A unique integer value identifying this S3 Access Key.
     */
    id: number;
    data: S3AccessKey;
  }
}

export { S3Service }
