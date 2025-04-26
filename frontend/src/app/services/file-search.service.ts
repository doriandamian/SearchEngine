import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, retry } from 'rxjs';
import { Query } from '../models/query.model';

@Injectable({
  providedIn: 'root',
})
export class FileSearchService {
  private apiUrl = 'http://127.0.0.1:5000/search';

  constructor(private httpClient: HttpClient) {}

  getFiles(query: Query): Observable<any[]> {
    let params = new HttpParams();

    if (query.path)
      for (const value of query.path) params = params.append('path', value);
    if (query.title)
      for (const value of query.title) params = params.append('title', value);
    if (query.extension)
      for (const value of query.extension)
        params = params.append('extension', value);
    if (query.contents)
      for (const value of query.contents)
        params = params.append('contents', value);

    return this.httpClient.get<any[]>(this.apiUrl, { params });
  }
}
