from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanelItem

from editorcontainer.editor.editor import Editor
from editorcontainer.linenumbersstrip.linenumbersstrip import LineNumbersStrip

class EditorContainer(BoxLayout):
   
   line_numbers_strip = ObjectProperty(None)
   editor = ObjectProperty(None)
   tabbed_panel = ObjectProperty(None)
   
   def build_editor_container(self, style_loader):
       
       self.style_loader = style_loader             
       
       self.editor.build_editor(self.style_loader.style_name, 
                                self.style_loader)          
       self.tabbed_panel.add_widget(TabbedPanelItem())
