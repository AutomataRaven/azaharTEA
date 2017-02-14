import os

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
       
        self.default_tab_mimetype = None
        self.default_tab_file_path = None                     
       
    def add_new_tab(self, mime_type=None, tab_name=None):
       
        editor = EditorTab()
        editor_content = EditorTabContent()
        editor.content = editor_content
        name = editor_content.editor.change_lexer(mime_type)
        
        editor.change_tab_name(tab_name)
       
        self.parent.footer.change_information({'highlight_menu': name})
       
        self.add_widget(editor)
       
        #TODO Change this to 'self.switch_to(editor, do_scroll=True) 
        # when kivy 1.9.2 releases
        self.switch_to(editor)
    
        return editor
        
    def build_default_tab(self):
    
        self.build_tab(self.default_tab_file_path, self.default_tab_mimetype)

    def build_tab(self, file_path, mimetype):
    
        text = ''
        dir_path = None
        file_name = None
        
        if file_path is not None:
        
            with open(file_path) as file:
                text = file.read()
                
            dir_path, file_name = os.path.split(file_path)
        
        editor_tab = self.add_new_tab(mimetype,
                         file_name)
                         
        editor_tab.content.editor.text = text
        
                   
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

    def change_tab_name(self, name=None):
        
        if name is not None:
            self.text = name

              
class EditorTabContent(BoxLayout):

    line_numbers_strip = ObjectProperty(None)
    editor = ObjectProperty(None)
    
