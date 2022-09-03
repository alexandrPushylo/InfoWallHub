import ctypes
import io
import json
from os import chdir, sep, path
from sys import argv
from PIL import Image, ImageDraw, ImageFont, ImageChops


#----------connecting preset-------------------------
# from preset_digital_clock import Preset
# from preset_simple_date import Preset

from preset_complex_date import ComplexDate as Preset

#-------------------------------------------------------


TETS_DIR = f"D:{sep}Temp{sep}t{sep}"

class REngine():
    preset_json_file = 'preset.json'
    work_img_name = 'canvas'
    work_img_path = f'{TETS_DIR}'
    format_img = 'jpeg'
    widget_set = []
    Preset = Preset

    def __init__(self) -> None:
        self._buffer = ctypes.create_unicode_buffer(360)
        self._byte_buffer = io.BytesIO()
        
        self.original_image_path = ''
        self.canvas = None
        self.canvas_path = f"{__class__.work_img_path}{__class__.work_img_name}"
        
        self.get_wall_to_buffer()
        self.push_img()
        self.init_preset()
        self.dump_preset()

    def dump_preset(self):
        preset = {}
        preset['name'] = self.preset.name
        preset['widgets'] = self.preset.type
        preset['module'] = self.preset.__module__
        with open(__class__.preset_json_file, 'w') as fp:
            json.dump(preset, fp)
        self.clean_canvas()
        self.preset.draw(self.canvas,'sys_wall.jpeg')
        

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
            position=(100,100)
            )
        
    def render(self):
        self.clean_canvas()
        self.preset.draw(self.canvas, self.canvas_path)
        self.put_wall_from_buffer()



def main():
    img = Image.new('RGB',size=(500,500))
    re = REngine()
    re.canvas = img
    re.canvas_path = None
    re.render()
    img.show()
    


if __name__ == '__main__':
    # main()
    pass
