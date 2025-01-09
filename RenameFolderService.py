from folder_watcher import CsvWatcher
from SMWinservice import SMWinservice

# PATH OF INTEREST:
# 実在するパスを指定しておかないと、サービス開始で失敗します
watched_path = r'C:\Coding\Folder Watcher Service\CSV Files'

# class that inherits from SMWinservice
# SMWinservice を継承した RenameFolderService クラス
class RenameFolderService(SMWinservice):
    _svc_name_ = 'RenameFolderService'
    _svc_display_name_ = 'Py Folder Observer'
    _svc_description_ = r'Observes and renames CSV files of particular folder: C:\Coding\Folder Watcher Service\CSV Files'

    # Override the three main methods: 
    # 3つのメインメソッドをオーバーライドします
    def start(self):
        '''When start winservice is pressed'''
        self.isrunning = True
        self.stop_requested = False
    
    def stop(self):
        '''When winservice is stopped'''
        self.stop_requested = True
        self.service.stop() #call self.service.stop() - CsvWatcher.stop()
        self.isrunning = False
        self.iswaching = False

    def main(self):            

        '''When winservice is running, do below'''
        self.iswaching = False
        # Store class with path argument as self.service
        self.service = CsvWatcher(watched_path)
        while self.isrunning:
            if not self.iswaching:
                # サービス停止時に、RuntimeError("threads can only be started once") を回避するために追加
                if not self.isrunning: # when self.stop() method is called
                    break
                self.service.run() #call self.service.run() method
            self.iswaching = True

# entry point
# エントリーポイント
if __name__ == '__main__':
    RenameFolderService.parse_command_line()