import kivy
kivy.require('1.9.1')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty

from editorcontainer.editorcontainer import EditorContainer
from menubar.menubar import MenuBar
from footer.footer import Footer
from kivyloader import load_all_kv_files


class Container(BoxLayout):

    menu_bar = ObjectProperty(None)
    editor_container = ObjectProperty(None)
    footer = ObjectProperty(None)
    
    def build_text_editor(self):
             
        # Send editorcontainer to menubar and from there propapagate it
        self.menu_bar.propagate_editor_container(self.editor_container)

class AzaharTEAApp(App):
 
    columns = NumericProperty(10)
    rows = NumericProperty(1)   
    
    def build(self):
        
        load_all_kv_files()
        
        container = Container()
        container.build_text_editor()
        
        return container
        
        
if __name__ == '__main__':
    AzaharTEAApp().run()

