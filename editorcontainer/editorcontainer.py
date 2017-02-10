from kivy.uix.boxlayout import BoxLayout

from editorcontainer.editor.editor import Editor
from editorcontainer.linenumbersstrip.linenumbersstrip import LineNumbersStrip

class EditorContainer(BoxLayout):
   
   def __init__(self, style_loader, **kwargs):
       
       super(EditorContainer, self).__init__(**kwargs)
       self.style_loader = style_loader
   
   def build_editor_container(self):
       
       ln_strip = LineNumbersStrip()
       self.add_widget(ln_strip)
       
       editor = Editor(self.style_loader.style_name, self.style_loader,
                       **self.style_loader.style)
       self.add_widget(editor)
