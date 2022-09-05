import PresetConstr
import psutil


class MemoryUsage(PresetConstr.Preset):
    def __init__(self, preset_name=None, preset_type=None, position=None, font=None, size=50, fill=None):
        preset_name = "Usage memory"
        preset_type = "ram"
        super().__init__(preset_name, preset_type, position, font, size, fill)
    
    
    def get_size(self, bytes, suffix='B'):
        factor = 1024
        for unit in ['', 'K', 'M', 'G', 'T', 'P']:
            if bytes < factor:
                return f"{bytes:.2f} {unit}{suffix}"
            bytes /= factor
    
    def set_context(self):
        svmem = psutil.virtual_memory()
        self.context = f"""
        Объем: {self.get_size(svmem.total)}
        Доступно: {self.get_size(svmem.available)}
        Используется: {self.get_size(svmem.used)}
        Процент: {svmem.percent}%"""
        return super().set_context()
    
if __name__ == "__main__":
    MemoryUsage().show_preset() 