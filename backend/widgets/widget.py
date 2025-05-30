from abc import ABC, abstractmethod

class Widget(ABC):
    @abstractmethod
    def command(self):
        pass

    @abstractmethod
    def can_activate(self, query, results) -> bool:
        pass

class AnalyzeLogsWidget(Widget):
    def command(self):
        return "analyze_logs"
    
    def can_activate(self, query=None, results=None):
        extensions = [r[2].lower() for r in results if len(r) > 1 and isinstance(r[1], str)]
        log_count = sum(1 for extension in extensions if extension == '.log')
        return log_count > len(results) * 0.75 if results else False
    
class GalleryViewWidget(Widget):
    def command(self):
        return 'gallery_view'
    
    def can_activate(self, query=None, results=None):
        extensions = [r[2].lower() for r in results if len(r) > 1 and isinstance(r[1], str)]
        img_count = sum(1 for extension in extensions if extension in ['.jpg', '.jpeg', '.png', '.gif'])
        return img_count > len(results) * 0.75 if results else False
    
class TextEditorWidget(Widget):
    def command(self):
        return 'text_editor'
    
    def can_activate(self, query=None, results=None):
        extensions = [r[2].lower() for r in results if len(r) > 1 and isinstance(r[1], str)]
        txt_count = sum(1 for extension in extensions if extension in ['.txt', '.md', '.json'])
        return txt_count > len(results) * 0.75 if results else False
    
class DocsViewWidget(Widget):
    TRIGGER_KEYWORDS = ['docs', 'help', 'guide', 'readme', 'instruction', 'manual']

    def command(self):
        return 'doc_view'
    
    def can_activate(self, query=None, results=None):
        if results == None or results == []:
            return False
        title_terms = query.get("title", [])
        content_terms = query.get("contents", [])
        terms = title_terms + content_terms
        for term in terms:
            if any(trigger in term.lower() for trigger in self.TRIGGER_KEYWORDS):
                return True
        return False