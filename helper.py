from pathlib import Path

def getFolderName(path):
    return Path(path).name

def getFileName(path):
    return Path(path).name

def getFileNameWithoutExtension(file_path):
    return Path(file_path).stem