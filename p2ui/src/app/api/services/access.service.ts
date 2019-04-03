/* tslint:disable */
import { Injectable } from '@angular/core';
import { HttpClient, HttpRequest, HttpResponse, HttpHeaders } from '@angular/common/http';
import { BaseService as __BaseService } from '../base-service';
import { ApiConfiguration as __Configuration } from '../api-configuration';
import { StrictHttpResponse as __StrictHttpResponse } from '../strict-http-response';
import { Observable as __Observable } from 'rxjs';
import { map as __map, filter as __filter } from 'rxjs/operators';

import { AccessRule } from '../models/access-rule';
@Injectable({
  providedIn: 'root',
})
class AccessService extends __BaseService {
  static readonly accessRuleListPath = '/access/rule/';
  static readonly accessRuleCreatePath = '/access/rule/';
  static readonly accessRuleReadPath = '/access/rule/{id}/';
  static readonly accessRuleUpdatePath = '/access/rule/{id}/';
  static readonly accessRulePartialUpdatePath = '/access/rule/{id}/';
  static readonly accessRuleDeletePath = '/access/rule/{id}/';

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
   * @param params The `AccessService.AccessRuleListParams` containing the following parameters:
   *
   * - `offset`: The initial index from which to return the results.
   *
   * - `limit`: Number of results to return per page.
   */
  accessRuleListResponse(params: AccessService.AccessRuleListParams): __Observable<__StrictHttpResponse<{count: number, next?: null | string, previous?: null | string, results: Array<AccessRule>}>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;
    if (params.offset != null) __params = __params.set('offset', params.offset.toString());
    if (params.limit != null) __params = __params.set('limit', params.limit.toString());
    let req = new HttpRequest<any>(
      'GET',
      this.rootUrl + `/access/rule/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<{count: number, next?: null | string, previous?: null | string, results: Array<AccessRule>}>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `AccessService.AccessRuleListParams` containing the following parameters:
   *
   * - `offset`: The initial index from which to return the results.
   *
   * - `limit`: Number of results to return per page.
   */
  accessRuleList(params: AccessService.AccessRuleListParams): __Observable<{count: number, next?: null | string, previous?: null | string, results: Array<AccessRule>}> {
    return this.accessRuleListResponse(params).pipe(
      __map(_r => _r.body as {count: number, next?: null | string, previous?: null | string, results: Array<AccessRule>})
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param data undefined
   */
  accessRuleCreateResponse(data: AccessRule): __Observable<__StrictHttpResponse<AccessRule>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;
    __body = data;
    let req = new HttpRequest<any>(
      'POST',
      this.rootUrl + `/access/rule/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<AccessRule>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param data undefined
   */
  accessRuleCreate(data: AccessRule): __Observable<AccessRule> {
    return this.accessRuleCreateResponse(data).pipe(
      __map(_r => _r.body as AccessRule)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param id A unique integer value identifying this access rule.
   */
  accessRuleReadResponse(id: number): __Observable<__StrictHttpResponse<AccessRule>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    let req = new HttpRequest<any>(
      'GET',
      this.rootUrl + `/access/rule/${id}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<AccessRule>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param id A unique integer value identifying this access rule.
   */
  accessRuleRead(id: number): __Observable<AccessRule> {
    return this.accessRuleReadResponse(id).pipe(
      __map(_r => _r.body as AccessRule)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `AccessService.AccessRuleUpdateParams` containing the following parameters:
   *
   * - `id`: A unique integer value identifying this access rule.
   *
   * - `data`:
   */
  accessRuleUpdateResponse(params: AccessService.AccessRuleUpdateParams): __Observable<__StrictHttpResponse<AccessRule>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    __body = params.data;
    let req = new HttpRequest<any>(
      'PUT',
      this.rootUrl + `/access/rule/${params.id}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<AccessRule>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `AccessService.AccessRuleUpdateParams` containing the following parameters:
   *
   * - `id`: A unique integer value identifying this access rule.
   *
   * - `data`:
   */
  accessRuleUpdate(params: AccessService.AccessRuleUpdateParams): __Observable<AccessRule> {
    return this.accessRuleUpdateResponse(params).pipe(
      __map(_r => _r.body as AccessRule)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `AccessService.AccessRulePartialUpdateParams` containing the following parameters:
   *
   * - `id`: A unique integer value identifying this access rule.
   *
   * - `data`:
   */
  accessRulePartialUpdateResponse(params: AccessService.AccessRulePartialUpdateParams): __Observable<__StrictHttpResponse<AccessRule>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    __body = params.data;
    let req = new HttpRequest<any>(
      'PATCH',
      this.rootUrl + `/access/rule/${params.id}/`,
      __body,
      {
        headers: __headers,
        params: __params,
        responseType: 'json'
      });

    return this.http.request<any>(req).pipe(
      __filter(_r => _r instanceof HttpResponse),
      __map((_r) => {
        return _r as __StrictHttpResponse<AccessRule>;
      })
    );
  }
  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param params The `AccessService.AccessRulePartialUpdateParams` containing the following parameters:
   *
   * - `id`: A unique integer value identifying this access rule.
   *
   * - `data`:
   */
  accessRulePartialUpdate(params: AccessService.AccessRulePartialUpdateParams): __Observable<AccessRule> {
    return this.accessRulePartialUpdateResponse(params).pipe(
      __map(_r => _r.body as AccessRule)
    );
  }

  /**
   * Viewset that only lists events if user has 'view' permissions, and only
   * allows operations on individual events if user has appropriate 'view', 'add',
   * 'change' or 'delete' permissions.
   * @param id A unique integer value identifying this access rule.
   */
  accessRuleDeleteResponse(id: number): __Observable<__StrictHttpResponse<null>> {
    let __params = this.newParams();
    let __headers = new HttpHeaders();
    let __body: any = null;

    let req = new HttpRequest<any>(
      'DELETE',
      this.rootUrl + `/access/rule/${id}/`,
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
   * @param id A unique integer value identifying this access rule.
   */
  accessRuleDelete(id: number): __Observable<null> {
    return this.accessRuleDeleteResponse(id).pipe(
      __map(_r => _r.body as null)
    );
  }
}

module AccessService {

  /**
   * Parameters for accessRuleList
   */
  export interface AccessRuleListParams {

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
   * Parameters for accessRuleUpdate
   */
  export interface AccessRuleUpdateParams {

    /**
     * A unique integer value identifying this access rule.
     */
    id: number;
    data: AccessRule;
  }

  /**
   * Parameters for accessRulePartialUpdate
   */
  export interface AccessRulePartialUpdateParams {

    /**
     * A unique integer value identifying this access rule.
     */
    id: number;
    data: AccessRule;
  }
}

export { AccessService }
