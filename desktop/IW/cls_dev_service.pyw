import json
from os import sep, path

from datetime import datetime
from time import sleep

from R_engine import REngine 

BUFFER = f"D:{sep}Temp{sep}t{sep}buffer.txt"

class IWService():
    buffer = "buffer"
    frequency = 1
        
    def __init__(self) -> None:
        self.buffer = __class__.buffer
        self.settings = {}
        self.read_buffer()
        self.get_status()
    
    def read_buffer(self):
        try:
            with open(self.buffer, 'r') as fp:
                self.settings = json.load(fp)
        except Exception as e:
            print(e)
            
    def get_status(self):
        self.read_buffer()
        self.status = self.settings.get('status', False)
        return self.status
    
    def waiting(self):
        freq = self.settings.get('frequency', __class__.frequency)
        sleep(freq)
        
              
def main():
    iwservice = IWService()
    rend = REngine()
            
    while iwservice.get_status():
                        
        rend.render()
        
        iwservice.waiting()
    rend.restore_wall()
    
    
    
if __name__ == '__main__':
    main()