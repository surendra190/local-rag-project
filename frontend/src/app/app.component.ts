import { Component, inject } from '@angular/core';

import { CommonModule } from '@angular/common';

import { FormsModule } from '@angular/forms';

import { ApiService, DocumentItem } from './services/api.service';

@Component({
  selector: 'app-root',

  standalone: true,

  imports: [CommonModule, FormsModule],

  templateUrl: './app.component.html',
})
export class AppComponent {
  private api = inject(ApiService);

  documents: DocumentItem[] = [];

  question = '';

  answer = '';

  sources: any[] = [];

  uploading = false;

  asking = false;

  message = '';

  constructor() {
    this.loadDocuments();
  }

  loadDocuments() {
    this.api.listDocuments().subscribe({
      next: (documents) => {
        this.documents = documents;
      },

      error: () => {
        this.message = 'Backend not reachable';
      },
    });
  }

  onFile(event: Event) {
    const input = event.target as HTMLInputElement;

    const file = input.files?.[0];

    if (!file) {
      return;
    }

    this.uploading = true;

    this.message = 'Uploading and indexing...';

    this.api.upload(file).subscribe({
      next: () => {
        this.message = 'Document indexed successfully';

        this.uploading = false;

        this.loadDocuments();
      },

      error: (error) => {
        this.message = error.error?.detail || 'Upload failed';

        this.uploading = false;
      },
    });
  }

  ask() {
    if (!this.question.trim()) {
      return;
    }

    this.asking = true;

    this.answer = '';

    this.api.chat(this.question).subscribe({
      next: (response) => {
        this.answer = response.answer;

        this.sources = response.sources;

        this.asking = false;
      },

      error: (error) => {
        this.answer = error.error?.detail || 'Question failed';

        this.asking = false;
      },
    });
  }
}
