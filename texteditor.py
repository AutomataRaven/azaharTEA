from kivy.app import App

from styles.styleloader import StyleLoader
from editorcontainer.editor.editor import Editor

class TextEditorApp(App):
    
    def build(self):
        
        self.style_loader = StyleLoader()
        
        editor = Editor(self.style_loader.style_name, self.style_loader,
            **self.style_loader.style)
       
        return editor
        
        

if __name__ == '__main__':
    TextEditorApp().run()

