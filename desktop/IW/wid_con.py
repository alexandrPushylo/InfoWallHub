from PIL import Image, ImageDraw, ImageFont

from datetime import datetime

class Widget():
    
    def __init__(
        self, 
        widget_name='demo', 
        widget_type='demo', 
        position=(0,0),
        font='arial.ttf',
        size = 72,
        fill=(255,255,255)
        
        ):
        
        self.name = widget_name
        self.type = widget_type
        self.position = position
        self.font = font
        self.size = size
        self.fill = fill
        self.context = 'DEMO'
        
        
        
    def set_context(self):
        self.context = str(datetime.today().time())[:-7]
        
        
    
            
    
    def draw(self, canvas:Image, canvas_path:str):
        self.set_context()
        font = ImageFont.truetype(self.font, self.size)
        
        canv = ImageDraw.Draw(canvas)
        canv.text(self.position, self.context, self.fill, font)
        
        if canvas_path != None:
            canvas.save(canvas_path, format='jpeg')
    
    # def save(self, path):
    #     if path != None:
            
    #         pass


def show():
    img = Image.new('RGB',size=(500,500))
    widget = Widget()
    widget.draw(img, None)
    img.show()

if __name__ == "__main__":
    show()