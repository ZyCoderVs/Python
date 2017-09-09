import os

def MkDirDown(name):
    dirPath='E:\\MMPic'+'\\'+name
    if os.path.exists(dirPath):
        print('%s目录已经存在'%(name))
    else:
        os.mkdir(dirPath)