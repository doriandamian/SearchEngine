import { Component } from '@angular/core';
import { FileSearchService } from './services/file-search.service';
import { FormsModule } from '@angular/forms';
import { SearchComponent } from "./search/search.component";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule, SearchComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  title = 'SearchEngine';
}
