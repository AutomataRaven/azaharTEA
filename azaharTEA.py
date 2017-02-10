import kivy
kivy.require('1.9.1')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from styles.styleloader import StyleLoader
from editorcontainer.editorcontainer import EditorContainer
from menubar.menubar import MenuBar
from footer.footer import Footer
from kivyloader import load_all_kv_files


class Container(BoxLayout):


    def build_text_editor(self):
    
        self.style_loader = StyleLoader()       
       
        menu_bar = MenuBar()
        self.add_widget(menu_bar)
        
        editor_container = EditorContainer(self.style_loader)
        editor_container.build_editor_container()      
        self.add_widget(editor_container)
        
        footer = Footer()
        self.add_widget(footer)
              

class AzaharTEAApp(App):
    
    
    def build(self):
        
        load_all_kv_files()
        
        container = Container()
        container.build_text_editor()
        
        return container
        
        

if __name__ == '__main__':
    AzaharTEAApp().run()

