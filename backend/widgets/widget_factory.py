from typing import List, Dict
from .widget import Widget, AnalyzeLogsWidget, GalleryViewWidget, TextEditorWidget, DocsViewWidget

class WidgetFactory:
    def __init__(self):
        self._widgets: List[Widget] = [
            AnalyzeLogsWidget(),
            GalleryViewWidget(),
            TextEditorWidget(),
            DocsViewWidget()
        ]

    def get_widgets(self, query: Dict, results: List[Dict]):
        active = []
        for widget in self._widgets:
            if widget.can_activate(query, results):
                active.append(widget.command())
        print(active)
        return active