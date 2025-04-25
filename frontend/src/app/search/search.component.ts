import { Component, inject } from '@angular/core';
import { FileSearchService } from '../services/file-search.service';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './search.component.html',
  styleUrl: './search.component.scss',
})
export class SearchComponent {
  searchQuery: string = '';
  files: any[] = [];
  errorMessage = '';

  private searchService = inject(FileSearchService);

  onSearch() {
    if (!this.searchQuery) {
      return;
    }
    this.searchService.getFiles(this.searchQuery).subscribe(
      (response) => {
        this.files = response;
      },
      (error) => {
        console.error('Error fetching files');
      }
    );
  }
}
