import ctypes
import io
import json
import importlib

from os import chdir, sep, path
from PIL import Image

from PresetConstr import Preset #Demo mode


class REngine():
    SETTINGS = 'settings.json'
    file_preview_name = 'sys_wall.jpeg' #self.preset_conf['file_preview'] = "sys_wall.jpeg"
    preset_json_file = 'preset.json'    #self.settings['preset_config_file'] = "preset.json"
    work_img_name = 'canvas'
    work_img_path = ''
    format_img = 'jpeg'
    widget_set = []
    Preset = Preset

    def __init__(self) -> None:
        self.read_settings()
        self.install_preset()
        
        self._buffer = ctypes.create_unicode_buffer(360)
        self._byte_buffer = io.BytesIO()
        
        self.original_image_path = ''
        self.canvas = None
        self.canvas_path =f"{path.dirname(__file__)}{sep}{__class__.work_img_name}"
        
        self.get_wall_to_buffer()
        self.push_img()
        self.init_preset()
        self.dump_preset()


    def read_settings(self):
        #read setting.json
        try:
            with open(__class__.SETTINGS, 'r') as fp:
                self.settings = json.load(fp)
        except Exception as e:
            print(e)
        #read preset.json    
        try:
            preset_conf_name = self.settings.get('preset_config_file', __class__.preset_json_file)
            with open(preset_conf_name, 'r') as fp:
                self.preset_conf = json.load(fp)
        except:
            print("Demo mode")
            
    
    def install_preset(self):
        try:
            preset_module = self.preset_conf['module']
            preset_class = self.preset_conf['class_name']
            __class__.Preset = getattr(importlib.import_module(preset_module),preset_class)
        except:
            __class__.Preset = Preset
        
        
    def dump_preset(self):
        preset = {}
        preset['name'] = self.preset.name
        preset['widgets'] = self.preset.type
        preset['module'] = self.preset.__module__
        preset['class_name'] = self.preset.__class__.__name__
        preset['file_preview'] = __class__.file_preview_name     
        with open(__class__.preset_json_file, 'w') as fp:
            json.dump(preset, fp)
        self.clean_canvas()
        self.preset.draw(self.canvas, __class__.file_preview_name)
        

    def get_wall_to_buffer(self):
        ctypes.windll.user32.SystemParametersInfoW(0x0073 , 260, self._buffer, 0)
        self.original_image_path = self._buffer.value
        
    def push_img(self):
        original_img = Image.open(self._buffer.value)
        original_img.save(self._byte_buffer, format=__class__.format_img)
               
    def put_wall_from_buffer(self):# put wall
        try:
            if self.canvas_path != None:
                ctypes.windll.user32.SystemParametersInfoW(0x0014 , 0, self.canvas_path, 0)
        except:
            pass
        
    def restore_wall(self): #restore wall
        try:
            ctypes.windll.user32.SystemParametersInfoW(0x0014 , 0, self.original_image_path, 0)
        except:
            pass
        
    def clean_canvas(self):
        self.canvas = Image.open(self._byte_buffer)            
            
    # def compare_img(self, image1, image2):
    #     image1 = Image.open(image1)
    #     image2 = Image.open(image2)
    #     diff = ImageChops.difference(image1, image2)
    #     if diff.getbbox() == None:
    #         return True
    #     else:
    #         return False
    
    def init_preset(self):
        self.preset = __class__.Preset(
            position=(100,100),
            size=46
            )
        
        
    def render(self):
        self.clean_canvas()
        self.preset.draw(self.canvas, self.canvas_path)
        self.put_wall_from_buffer()



def main():
    chdir(path.dirname(__file__))
    re = REngine()
    print(
        re.settings,
        re.canvas,
        re.canvas_path,
        re.original_image_path,
        sep='\n'
        )
    


if __name__ == '__main__':
    main()
    