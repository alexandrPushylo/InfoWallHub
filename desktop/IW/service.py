from win32.lib import win32serviceutil
from win32 import win32service
from win32 import win32event
from win32 import servicemanager
import socket

class AppServerSvc(win32serviceutil.ServiceFramework):
    _svc_name = "TestService" 
    _svc_display_name_ = "Test Service"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        
    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()
        
    def main(self):
        pass
    
    if __name__ == '__main__':
        win32serviceutil.HandleCommandLine(AppServerSvc)
