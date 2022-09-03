import PresetConstr
import datetime


class ComplexDate(PresetConstr.Preset):
    def __init__(self, preset_name=None, preset_type=None, position=None, font=None, size=None, fill=None):
        preset_name = 'Complex date'
        preset_type = 'date, time'
        super().__init__(preset_name, preset_type, position, font, size, fill)
    
    def init(self):
        import locale
        locale.setlocale(
            category=locale.LC_ALL,
            locale="Russian"
        )
        
    def set_context(self):
        now = datetime.datetime.now()
        self.context = now.strftime("%H:%M:%S \n%d %B %Y\n%A\n")
        return super().set_context()

    
if __name__ == "__main__":
    ComplexDate.show_preset()
    