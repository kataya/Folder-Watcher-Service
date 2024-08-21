# How to create a Windows Service in Python
# https://thepythoncorner.com/posts/2018-08-01-how-to-create-a-windows-service-in-python/
'''
SMWinservice
by Davide Mastromatteo

Base class to create winservice in Python
Python で winservice を作成するための基底クラス
-----------------------------------------

Instructions:
手順:

1. Just create a new class that inherits from this base class
   この基底クラスを継承した新しいクラスを作成します
2. Define into the new class the variables
   新しいクラスに次の変数を定義する
   _svc_name_ = "nameOfWinservice"
                "Winserviceの名称"
   _svc_display_name_ = "name of the Winservice that will be displayed in scm"
                        "サービス コントロール マネージャー(scm)でのWinserviceの表示名"
   _svc_description_ = "description of the Winservice that will be displayed in scm"
                       "サービス コントロール マネージャー(scm)scmでのWinserviceの説明"
3. Override the three main methods:
   3つのメインメソッドをオーバーライドする
    def start(self) : if you need to do something at the service initialization.
                      A good idea is to put here the inizialization of the running condition
                      サービスの初期化時に何かをする必要がある場合のメソッド
                      実行状態の初期化をここにに置くのはいいアイディアです
    def stop(self)  : if you need to do something just before the service is stopped.
                      A good idea is to put here the invalidation of the running condition
                      サービスの停止する直前に何かをする必要がある場合のメソッド
                      実行状態の無効化をここに置いておくのがいいアイディアです
    def main(self)  : your actual run loop. Just create a loop based on your running condition
                      実際の実行ループ。実行条件に基づいてループを作成する。
4. Define the entry point of your module calling the method "parse_command_line" of the new class
   新しいクラスで"parse_command_line"のメソッドを呼び出し、モジュールのエントリーポイントを定義する
5. Enjoy
   楽しむ
'''

import socket
import win32serviceutil
import servicemanager
import win32event
import win32service

class SMWinservice(win32serviceutil.ServiceFramework):
    '''Base class to create winservice in Python'''
    _svc_name_ = 'pythonService'
    _svc_display_name_ = 'Python Service'
    _svc_description_ = 'Python Service Description'

    @classmethod
    def parse_command_line(cls):
        '''ClassMethod to parse the command line'''
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        '''Constructor of the winservice'''
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        '''Called when the service is asked to stop'''
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        '''Called when the service is asked to start'''
        self.start()        
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def start(self):
        '''Override to add logic before the start eg. running condition'''
        pass

    def stop(self):
        '''Override to add logic before the stop eg. invalidating running condition'''
        pass

    def main(self):
        '''Main class to be ovverridden to add logic'''
        pass

if __name__ == '__main__':
    SMWinservice.parse_command_line()