import PresetConstr
from datetime import datetime


class SimpleDate(PresetConstr.Preset):
    def __init__(self, preset_name=None, preset_type=None, position=None, font=None, size=None, fill=None):
        preset_name = 'Just a date'
        preset_type = 'date'
        super().__init__(preset_name, preset_type, position, font, size, fill)
    
    def set_context(self):
        today = datetime.now()  
        self.context = today.strftime("%d.%m.%Y")
        return super().set_context()
        
   
if __name__ == "__main__":
    SimpleDate.show_preset()    