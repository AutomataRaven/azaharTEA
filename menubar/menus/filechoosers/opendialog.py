import os
import mimetypes

from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


class OpenDialog(Popup):

    open_button = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel_button = ObjectProperty(None)
       
    def cancel(self):
        self.dismiss()
        
    def propagate_editor_container(self, editor_container):
        self.editor_container = editor_container
        
    
    def open_file(self, path):
           
        mimetype, encoding = mimetypes.guess_type(path)
                
        self.editor_container.build_tab(path, mimetype)
                                 
        self.cancel()
