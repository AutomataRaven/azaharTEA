from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.tabbedpanel import TabbedPanel

from editorcontainer.editor.editor import Editor
from editorcontainer.linenumbersstrip.linenumbersstrip import LineNumbersStrip


class EditorContainer(TabbedPanel):   
   
   default_editor_tab = ObjectProperty(None)              
       
   def add_new_tab(self):
       
       editor = EditorTab()
       self.add_widget(editor)
       self.switch_to(editor)
            
              
class EditorTab(TabbedPanelItem):

    line_numbers_strip = ObjectProperty(None)
    editor = ObjectProperty(None)
