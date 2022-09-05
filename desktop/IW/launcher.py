import argparse
import json
import tarfile
from os import sep, path, mkdir
import sys
import subprocess


class Launcher():
        
    SETTINGS = 'settings.json'
    BUFFER = 'byffer'
        
    def __init__(self) -> None:
        self.read_settings()
        self.creat_works_space()
        
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
            with open(self.settings.get('buffer', __class__.BUFFER), 'w') as fp:
                json.dump(self.settings, fp)
        except Exception as e:
            print(e)
    
    def create_arch(self):
        param = {}
        with open('preset.json','r')as fp:
            param = json.load(fp)
        print(param['module'])      ###################
        with tarfile.open(f"{self.settings['presets_dir']}{sep}{param['module']}.tar",'w') as tar:
            tar.add(param['module']+'.py')
            tar.add(self.settings['preset_config_file'])
            tar.add(param['file_preview'])
    
   
    
    def install_preset(self, preset_arch_name:str):
        if path.isfile(f"{self.settings['presets_dir']}{sep}{preset_arch_name}"):
            preset_module_name = preset_arch_name.replace('tar','py') 
            with tarfile.open(f"{self.settings['presets_dir']}{sep}{preset_arch_name}", 'r') as tar:
                tar.extract(preset_module_name)
                tar.extract(self.settings['preset_config_file'])
            print(f"Пресет {preset_arch_name} установлен!")
        else:
            print(f"Данный пресет {preset_arch_name} не нейден!")
                

    def creat_works_space(self):
        if not path.isdir(self.settings['presets_dir']):
            mkdir(self.settings['presets_dir'])
        if not path.isdir(self.settings['workdir']):
            mkdir(self.settings['workdir'])
        
        
        
def parse_cml():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--command',type=str)
    parser.add_argument('-i','--install', required=False,type=str)
    args = parser.parse_args()
    print(args)#######
    return args
        
def main():
    args = parse_cml()
    launch = Launcher()

    comm = str(args.command).lower()
    
    if comm == 'start': launch.start()
    elif comm == 'stop': launch.stop()
    elif comm == 'arch': launch.create_arch()
    elif args.install != '': launch.install_preset(args.install)
    elif comm == '': pass
    elif comm == '': pass
    elif comm == '': pass
    elif comm == '': pass
    
    else:
        print(comm)
   

if __name__ == '__main__':
    main()