import { Component, inject, OnInit } from '@angular/core';
import { FileSearchService } from '../services/file-search.service';
import { FormsModule } from '@angular/forms';
import { Query } from '../models/query.model';
import { WidgetGeneratorComponent } from "./widget-generator/widget-generator.component";

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [FormsModule, WidgetGeneratorComponent],
  templateUrl: './search.component.html',
  styleUrl: './search.component.scss',
})
export class SearchComponent implements OnInit {
  path: string = '';
  title: string = '';
  extension: string = '';
  contents: string = '';

  files: any[] = [];
  widgets: any[] = [];

  pathSuggestions: string[] = [];
  titleSuggestions: string[] = [];
  extensionSuggestions: string[] = [];
  contentsSuggestions: string[] = [];

  private searchService = inject(FileSearchService);

  ngOnInit(): void {
    this.getSearchHistory();
  }

  getSearchHistory(): void {
    this.searchService.getSearchHistory().subscribe(
      (history) => {
        this.updateSuggestions(history);
      },
      (error) => {
        console.error('Error fetching search history', error);
      }
    );
  }

  updateSuggestions(searchHistory: string[]): void {
    this.pathSuggestions = [];
    this.titleSuggestions = [];
    this.extensionSuggestions = [];
    this.contentsSuggestions = [];

    // Loop through the search history and categorize them
    searchHistory.forEach(([keyword, category]) => {
      switch (category) {
        case 'path':
          this.pathSuggestions.push(keyword);
          break;
        case 'title':
          this.titleSuggestions.push(keyword);
          break;
        case 'extension':
          this.extensionSuggestions.push(keyword);
          break;
        case 'content':
          this.contentsSuggestions.push(keyword);
          break;
        default:
          console.warn(`Unknown category: ${category}`);
      }
    });
  }

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

    this.searchService.search(query).subscribe(
      (response) => {
        this.files = response['result'];
        this.widgets = response['widgets'];
        console.log(this.widgets);
      },
      (error) => {
        console.error('Error fetching files', error);
      }
    );
  }
}
