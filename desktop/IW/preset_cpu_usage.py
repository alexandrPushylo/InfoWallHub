import PresetConstr
import psutil


class CPUUsage(PresetConstr.Preset):
    def __init__(self, preset_name=None, preset_type=None, position=None, font=None, size=50, fill=None):
        preset_name = "CPU usage"
        preset_type = "cpu"
        super().__init__(preset_name, preset_type, position, font, size, fill)
    
    
    def get_size(self, bytes, suffix='B'):
        factor = 1024
        for unit in ['', 'K', 'M', 'G', 'T', 'P']:
            if bytes < factor:
                return f"{bytes:.2f} {unit}{suffix}"
            bytes /= factor
    
    def set_context(self):
        cpufreq = psutil.cpu_freq()
        self.context = f"""
        Физические ядра: {psutil.cpu_count(logical=False)}
        Всего ядер: {psutil.cpu_count(logical=True)}
        
        Максимальная частота: {cpufreq.max:.2f}МГц
        Минимальная частота: {cpufreq.min:.2f}МГц
        Чекущая частота: {cpufreq.current:.2f}МГц
        """
        return super().set_context()
    
if __name__ == "__main__":
    CPUUsage().show_preset() 