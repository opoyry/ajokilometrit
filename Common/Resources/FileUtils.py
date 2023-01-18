import os
import shutil

def MoveDownloadedFile(encryptedFileName, destinationPath):
    homeDir = os.path.expanduser("~")
    print('homeDir', homeDir)
    downloadedFileWithPath = os.path.join(homeDir, "Downloads", encryptedFileName)
    print('downloadedFileWithPath', downloadedFileWithPath)
    print('homeDir', os.listdir(homeDir)) 
    shutil.move(downloadedFileWithPath, destinationPath)