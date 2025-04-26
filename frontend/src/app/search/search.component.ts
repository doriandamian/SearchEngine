import { Component, inject } from '@angular/core';
import { FileSearchService } from '../services/file-search.service';
import { FormsModule } from '@angular/forms';
import { Query } from '../models/query.model';

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './search.component.html',
  styleUrl: './search.component.scss',
})
export class SearchComponent {
  path: string = '';
  title: string = '';
  extension: string = '';
  contents: string = '';

  files: any[] = [];

  private searchService = inject(FileSearchService);

  onSearch() {
    let query = new Query();

    if (this.path.trim()) {
      query.path = this.path
        .trim()
        .split(',')
        .map((p) => p.trim());
    }
    if (this.title.trim()) {
      query.title = this.title
        .trim()
        .split(',')
        .map((t) => t.trim());
    }
    if (this.extension.trim()) {
      query.extension = this.extension
        .trim()
        .split(',')
        .map((e) => e.trim());
    }
    if (this.contents.trim()) {
      query.contents = this.contents
        .trim()
        .split(',')
        .map((c) => c.trim());
    }

    console.log('Sending Query: ', query);

    this.searchService.getFiles(query).subscribe(
      (response) => {
        this.files = response;
      },
      (error) => {
        console.error('Error fetching files', error);
      }
    );
  }
}
