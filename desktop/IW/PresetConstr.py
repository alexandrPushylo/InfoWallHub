from PIL import Image, ImageDraw, ImageFont

class Preset():
    position=(0,0)
    fill=(255,255,255)
    name = 'demo'
    w_type = 'demo'
    font = 'arial.ttf'
    size = 24
    
    def __init__(self, preset_name=None, preset_type=None, position=None, font=None, size = None, fill=None):
        self.name = preset_name if preset_name != None else __class__.name
        self.type = preset_type if preset_type != None else __class__.w_type
        self.position = position if position != None else __class__.position
        self.font = font if font != None else __class__.font
        self.size = size if size != None else __class__.size
        self.fill = fill if fill != None else __class__.fill
        self.context = 'DEMO'
        self.init()
        
    def init(self):
        pass
        
    def set_context(self):
        self.context = str(self.context)
    
    def draw(self, canvas, canvas_path):
        self.set_context()
        font = ImageFont.truetype(self.font, self.size)
        canv = ImageDraw.Draw(canvas)
        canv.text(self.position, self.context, self.fill, font)
        if canvas_path != None:
            canvas.save(canvas_path, format='jpeg')
    
    @classmethod
    def show_preset(cls):
        img = Image.new('RGB',size=(1000,1000))
        preset = cls()
        preset.draw(img, None)
        print(f"{preset.name=}\n{preset.type=}")
        img.show()         


if __name__ == "__main__":
    Preset.show_preset()  
    