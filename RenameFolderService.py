from folder_watcher import CsvWatcher
from SMWinservice import SMWinservice

# PATH OF INTEREST:
watched_path = r'C:\Coding\Folder Watcher Service\CSV Files'

# class that inherits from SMWinservice
class RenameFolderService(SMWinservice):
    _svc_name_ = 'RenameFolderService'
    _svc_display_name_ = 'Py Folder Observer'
    _svc_description_ = r'Observes and renames CSV files of particular folder: C:\Coding\Folder Watcher Service\CSV Files'

    # Override the three main methods: 
    def start(self):
        '''When start winservice is pressed'''
        self.isrunning = True

    def stop(self):
        '''When winservice is stopped'''
        self.service.stop() #call self.service.stop() method
        self.isrunning = False
        self.iswaching = False

    def main(self):
        '''When winservice is running, do below'''
        self.iswaching = False
        # Store class with path argument as self.service
        self.service = CsvWatcher(watched_path)
        while self.isrunning:
            if not self.iswaching:
                self.service.run() #call self.service.run() method
            self.iswaching = True

# entry point
if __name__ == '__main__':
    RenameFolderService.parse_command_line()