import { Component, Input, SimpleChange } from '@angular/core';

@Component({
  selector: 'app-widget-generator',
  imports: [],
  templateUrl: './widget-generator.component.html',
  styleUrl: './widget-generator.component.scss',
})
export class WidgetGeneratorComponent {
  @Input() command: string = '';

  widgetTitle: string = '';
  isValidCommand = false;

  private readonly widgetMap: { [key: string]: { title: string } } = {
    analyze_logs: { title: 'Analyze Logs' },
    gallery_view: { title: 'View as Gallery' },
    text_editor: { title: 'Open Text Editor' },
    doc_view: { title: 'Open Document Viewer' },
  };

  ngOnChanges(): void {
    const widget = this.widgetMap[this.command];
    if (widget) {
      this.widgetTitle = widget.title;
      this.isValidCommand = true;
    } else {
      this.isValidCommand = false;
    }
  }
}
