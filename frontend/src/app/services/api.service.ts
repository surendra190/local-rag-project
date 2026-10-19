import { Injectable, inject } from '@angular/core';

import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

export interface DocumentItem {
  id: string;

  filename: string;

  status: string;

  chunk_count: number;

  created_at: string;
}

export interface ChatResponse {
  answer: string;

  sources: {
    document_id: string;

    page: number;

    score: number;
  }[];
}

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private http = inject(HttpClient);

  private base = 'http://localhost:8000/api';

  listDocuments(): Observable<DocumentItem[]> {
    return this.http.get<DocumentItem[]>(`${this.base}/documents`);
  }

  upload(file: File): Observable<unknown> {
    const formData = new FormData();

    formData.append('file', file);

    return this.http.post(`${this.base}/documents/upload`, formData);
  }

  chat(question: string): Observable<ChatResponse> {
    return this.http.post<ChatResponse>(`${this.base}/chat`, {
      question,
    });
  }
}
