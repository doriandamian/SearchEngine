import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class FileSearchService {
  private apiUrl = 'http://127.0.0.1:5000/search';

  constructor(private httpClient: HttpClient) {}

  getFiles(query: string): Observable<any[]> {
    const params = new HttpParams().set('query', query);
    return this.httpClient.get<any[]>(this.apiUrl, {params});
  }
}
