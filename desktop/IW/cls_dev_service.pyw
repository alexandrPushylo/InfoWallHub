import json
from os import sep, path

from datetime import datetime
from time import sleep

from rend_engine import REngine

BUFFER = f"D:{sep}Temp{sep}t{sep}buffer.txt"

class IWService():
    buffer = "buffer.txt"
    frequency = 1
        
    def __init__(self, buffer) -> None:
        self.buffer = buffer
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
    iwservice = IWService(buffer=BUFFER)
    rend = REngine()
    
        
    while iwservice.get_status():
        with open(f"D:{sep}Temp{sep}t{sep}log.txt" , 'a+') as fp:
            fp.write(
                f"{str(datetime.now())[:-7]}\n"
                )
           
        rend.render()
        
        
        iwservice.waiting()
    rend.restore_wall()
    
    
    
if __name__ == '__main__':
    main()