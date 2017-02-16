import os

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.uix.scrollview import ScrollView

from editorcontainer.editor.editor import Editor


class CodeScrollView(ScrollView):

    line_numbers_strip = ObjectProperty(None)
    
    editor = ObjectProperty(None)
    
    layout = ObjectProperty(None)
    
    show_line_number = BooleanProperty(True)   
    
    def __init__(self, **kwargs):
        super(CodeScrollView, self).__init__(**kwargs)
        self.max_num_of_lines = 0
        self.editor.bind(focus=self.on_editor_focus)
        
        if not self.show_line_number:
            self.line_numbers_strip.parent.remove_widget(self.line_numbers_strip)
        else:
            self.editor.bind(_lines=self.on_lines_change)

    def on_editor_focus(self, *args):

        if args[1]:
            Window.bind(on_keyboard=self.on_keyboard)
        else:
            Window.unbind(on_keyboard=self.on_keyboard)

    def on_keyboard(self, keyboard, keycode, scancode, value, modifiers):
        
        # ctrl-s to save
        if keycode == 115 and value == 's':
            if 'ctrl' in modifiers and len(modifiers) == 1:
                self.editor.save_tab()

    def on_lines_change(self, widget, value):
    
        n = len(value)
        if n > self.max_num_of_lines:
            self.update_lines_number(self.max_num_of_lines, n)

    def on_show_line_number(self, instance, value):
        
        if value:
            self.line_numbers_strip.width = self.line_numbers_strip._label_cached.get_extents(
            str(self.max_num_of_lines))[0] + (self.line_numbers_strip.padding[0] * 2)
        else:
            self.line_numbers_strip.width = 0

    def update_lines_number(self, old, new):

        self.max_num_of_lines = new
        self.line_numbers_strip.text += \
                    '\n'.join([str(i) for i in range(old + 1, new + 1)]) + '\n'
        self.line_numbers_strip.width = self.line_numbers_strip._label_cached.get_extents(
            str(self.max_num_of_lines))[0] + (self.line_numbers_strip.padding[0] * 2)
        
        
class EditorContainer(TabbedPanel):   
   
      
    def __init__(self, **kwargs):
       
        super(EditorContainer, self).__init__()
       
        self.default_tab_mimetype = None
        self.default_tab_file_path = None                     
       
    def add_new_tab(self, mime_type=None, tab_name=None):
       
        editor_tab = EditorTab()       
        
        editor_content = CodeScrollView()

        editor_tab.content = editor_content
        name = editor_content.editor.change_lexer(mime_type)
        
        editor_tab.change_tab_name(tab_name)
       
        self.parent.footer.change_information({'highlight_menu': name})

        self.add_widget(editor_tab)
       
        #TODO Change this to 'self.switch_to(editor, do_scroll=True) 
        # when kivy 1.9.2 releases
        self.switch_to(editor_tab)

        editor = editor_tab.content.editor
        
        editor.propagate_editor_container(self)
            
        if tab_name is None:
            editor.text=' '
            editor.text=''
            editor.bind(text=editor.text_changed)
            
        return editor_tab
        
    def build_default_tab(self):
    
        self.build_tab(self.default_tab_file_path, self.default_tab_mimetype)

    def build_tab(self, file_path, mimetype):
    
        text = ''
        dir_path = None
        file_name = None
        
        if file_path is not None:

            try:
                   
                with open(file_path) as file:
                    text = file.read()                            
                        
            except PermissionError as err:
                print(err, "You don't have the required access rights"
                      " to read: {0}".format(path), sep = '\n')
                return
            except FileNotFoundError as err:
                print(err, "{}: not found".format(file_path), sep='\n')
                return
            except IsADirectoryError as err:
                print(err, "Cannot open a directory", sep = '\n')  
                return 
                
            dir_path, file_name = os.path.split(file_path)
          
        editor_tab = self.add_new_tab(mimetype,
                         file_name)
          
        editor =  editor_tab.content.editor
            
        editor._name = file_name
        editor._path = dir_path          
        editor.text = text
        
        editor.bind(text=editor.text_changed)
                                                      
class EditorTab(TabbedPanelHeader):
       
    close_button = ObjectProperty(None)
       
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
                            
