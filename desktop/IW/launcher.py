import argparse
import json
from os import sep, path, system
import sys
import subprocess

# BUFFER = f"D:{sep}Temp{sep}t{sep}buffer.txt"######

class Launcher():
    SETTINGS = 'settings.json'
    BUFFER = f"D:{sep}Temp{sep}t{sep}buffer.txt"######
    
    def __init__(self) -> None:
        self.read_settings()
        
    def start(self):
        self.settings['status'] = True
        self.write_buffer()
        subprocess.Popen(['python' ,'cls_dev_service.pyw'])
        print(f'STARTING --> ')
        
    def stop(self):
        self.settings['status'] = False
        self.write_buffer()
        print('STOPING')
        
    def read_settings(self):
        try:
            with open(__class__.SETTINGS, 'r') as fp:
                self.settings = json.load(fp)
        except Exception as e:
            print(e)
            
    def write_buffer(self):
        try:
            with open(__class__.BUFFER, 'w') as fp:
                json.dump(self.settings, fp)
        except Exception as e:
            print(e)
        
        
def parse_cml():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--command',type=str)
    args = parser.parse_args()
    print(args)#######
    return args
        
def main():
    args = parse_cml()
    launch = Launcher()

    comm = str(args.command).lower()
    
    if comm == 'start': launch.start()
    elif comm == 'stop': launch.stop()
    elif comm == '': pass
    else:
        print(comm)
   

if __name__ == '__main__':
    main()