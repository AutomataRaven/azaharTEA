from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.tabbedpanel import TabbedPanel

from editorcontainer.editor.editor import Editor
from editorcontainer.linenumbersstrip.linenumbersstrip import LineNumbersStrip


class EditorContainer(TabbedPanel):   
   
   default_editor_tab = ObjectProperty(None)
   
   def build_editor_container(self, style_loader):
       
       self.style_loader = style_loader             
             
       self.default_editor_tab.send_style(self.style_loader)
            
              
class EditorTab(TabbedPanelItem):

    line_numbers_strip = ObjectProperty(None)
    editor = ObjectProperty(None)
    
    def send_style(self, style_loader):
        self.editor.build_editor(style_loader.style_name, style_loader)
