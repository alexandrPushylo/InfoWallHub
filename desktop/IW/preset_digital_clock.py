import PresetConstr
from datetime import datetime


class DigitalClock(PresetConstr.Preset):
    def __init__(self, preset_name=None, preset_type=None, position=None, font=None, size=None, fill=None):
        widget_name = 'Digital clock'
        widget_type = 'clock'
        super().__init__(widget_name, widget_type, position, font, size, fill)
    
    def set_context(self):
        self.context = datetime.today().time().strftime("%H:%M:%S")
        
    
if __name__ == "__main__":
    DigitalClock.show_preset()