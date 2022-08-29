import ctypes
import io
from os import chdir, sep, path
from PIL import Image, ImageDraw, ImageFont, ImageChops

from datetime import datetime


TETS_DIR = f"D:{sep}Temp{sep}t{sep}"

class REngine():
    backup_img_name = 'original.jpeg'
    work_img_name = 'canvas'
    work_img_path = f'{TETS_DIR}'
    format_img = 'jpeg'
        
    def __init__(self) -> None:
        self.buffer = ctypes.create_unicode_buffer(360)
        self.original_img = None
        self.work_img = None
        self.orig_path = ''
        self.bbb = io.BytesIO()
        self.canvas_path = f"{__class__.work_img_path}{__class__.work_img_name}"
        self.init()
        # self.bt()
    
    def get_wall_to_buffer(self):   #read wall
        ctypes.windll.user32.SystemParametersInfoW(0x0073 , 260, self.buffer, 0)
        self.orig_path = self.buffer.value
        
    def push_img(self):
        self.original_img = Image.open(self.buffer.value)
        # self.original_img.save(TETS_DIR+__class__.backup_img_name)
        self.original_img.save(self.bbb, format=__class__.format_img)
               
    def put_wall_from_buffer(self):# put wall
        try:
            ctypes.windll.user32.SystemParametersInfoW(0x0014 , 0, self.canvas_path, 0)#return True if ok
        except:
            pass
        
    def restore_wall(self): #restore wall
        try:
            ctypes.windll.user32.SystemParametersInfoW(0x0014 , 0, self.orig_path, 2)
        except:
            pass
        
    # def create_canvas(self):#####---------------------
    #     try:
    #         with open(TETS_DIR+__class__.backup_img_name, 'rb') as buffer:
    #             with open(self.canvas_path, 'wb') as img:
    #                 img.write(buffer.read())
    #         self.work_img = Image.open(self.canvas_path)
    #     except Exception as e:
    #         print(e)
            
    # def bt(self):####-------------------
    #     # with open(self.canvas_path, 'rb') as img:
    #     #     self.bbb = img.read
    #     self.work_img.save(self.bbb, format=__class__.format_img)
          
    def clean_canvas(self):
        self.work_img = Image.open(self.bbb)            
            
    def compare_img(self, image1, image2):
        image1 = Image.open(image1)
        image2 = Image.open(image2)
        diff = ImageChops.difference(image1, image2)
        if diff.getbbox() == None:
            return True
        else:
            return False
    
    def draw(self):
        now_time = str(datetime.today().time())[:-7]
        font = ImageFont.truetype('arial.ttf', size=72)
        
        # self.create_canvas()
        # self.work_img = self.sys_img.copy()
        self.clean_canvas()
        canvas = ImageDraw.Draw(self.work_img)
        canvas.text((0, 0), now_time, fill=(255, 255, 255), font=font)
        
        self.work_img.save(self.canvas_path,format=__class__.format_img)
        self.put_wall_from_buffer()

    def init(self):
        self.get_wall_to_buffer()
        self.push_img()
        # self.create_canvas()

def main():
    render = REngine()
    render.draw()
    
    render.restore_wall()#!!!!!!




if __name__ == '__main__':
    main()
