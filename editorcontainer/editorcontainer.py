from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from editorcontainer.editor.editor import Editor
from editorcontainer.linenumbersstrip.linenumbersstrip import LineNumbersStrip

class EditorContainer(BoxLayout):
   
   line_numbers_strip = ObjectProperty(None)
   editor = ObjectProperty(None)
   
   def build_editor_container(self, style_loader):
       
       self.style_loader = style_loader             
       
       self.editor.build_editor(self.style_loader.style_name, 
                                self.style_loader)          

