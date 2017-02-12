from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from editorcontainer.editor.editor import Editor
from editorcontainer.linenumbersstrip.linenumbersstrip import LineNumbersStrip


class EditorContainer(TabbedPanel):   
   
   def __init__(self, **kwargs):
       
       super(EditorContainer, self).__init__()
       
       editor = EditorTab()
       editor.content = EditorTabContent()
       
       self.add_widget(editor)               
       
   def add_new_tab(self):
       
       editor = EditorTab()
       editor.content = EditorTabContent()
       
       self.add_widget(editor)
       
       #TODO Change this to 'self.switch_to(editor, do_scroll=True) 
       # when kivy 1.9.2 releases
       self.switch_to(editor)
            
              
class EditorTab(TabbedPanelHeader):
       
    def close_editor_tab(self, widget):
     
        parent_panel = self.parent.tabbed_panel
        
        # Save the position to change tabs
        # in theory to the one on the left
        switch_index = parent_panel.tab_list.index(self)
        
        # See if the tab was the current one
        was_current = False or (self is parent_panel.current_tab)
        
        parent_panel.remove_widget(self)
        self.content.opacity = 0
        
        tab_list = parent_panel.tab_list
        
        # Find out if it's possible to change to other tab
        # and change to it
        tab_list_len = len(parent_panel.tab_list) 
        if(tab_list_len > 0):
        
            # Its not necessary if the tab wasn't the 'current_tab'            
            
            if was_current:
            
                #Calculate to position to switch to
                if not switch_index == tab_list_len:
                    switch_index = switch_index % tab_list_len
                else:
                    switch_index = tab_list_len - 1
                     
                parent_panel.switch_to(parent_panel.tab_list[switch_index])
                
class EditorTabContent(BoxLayout):

    line_numbers_strip = ObjectProperty(None)
    editor = ObjectProperty(None)
    
