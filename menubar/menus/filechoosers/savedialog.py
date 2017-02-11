from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty

import os

class SaveDialog(Popup):

    save_button = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel_button = ObjectProperty(None)
       
    def cancel(self):
        self.dismiss()
        
    def save(self, path, name):
    
        try:
            with open(os.path.join(path,name), 'w') as file:
                file.write('')
                    
        except PermissionError as err:
            print(err, "You don't have the required access rights"
                  " to write to: {0}".format(path), sep = '\n')
        except IsADirectoryError as err:
            print(err, "Cannot save file as directory", sep = '\n')        
        finally:
            self.cancel()