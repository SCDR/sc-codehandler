import os
import glob
import json

class FileHandler:
    def __init__(self,extensions=None,directory=None) -> None:
        curPath=os.path.abspath(__file__)
        parentPath=os.path.dirname(os.path.dirname(curPath))
        fileName="config.json"
        filePath=os.path.join(parentPath,fileName)
        with open(filePath,'r',encoding="utf-8") as file:
            try:
                config=json.load(file)
                codeFileConfig=config["codeFile"]
                self.extensions= extensions if extensions is not (None or "") else codeFileConfig["extensions"]
                self.directory = directory if directory is not (None or "") else codeFileConfig["directory"]
            except Exception as e:
                print("配置文件读取失败",e)
                exit()

    def findFilesWithExtension(self,directory=None, extensions=None):
        # 使用glob.glob()函数来查找指定目录下所有匹配的文件
        # '*'表示任意数量的字符，'*.txt'表示所有以.txt结尾的文件
        files=[]
        for root,dirs,filnames in os.walk(self.directory if directory is None else directory):
            for extension in self.extensions if extensions is None else extensions:
                files.extend(glob.glob(os.path.join(root, f"*.{extension}")))

        return files
    class BackwardsReader:
        """Read a file line by line, backwards"""

        BLKSIZE = 4096

        def __init__(self, file):
            self.file = file
            self.buf = ""
            self.file.seek(-1, 2)
            self.trailing_newline = 0
            lastchar = self.file.read(1)
            if lastchar == "\n":
                self.trailing_newline = 1
                self.file.seek(-1, 2)

        def readline(self):
            while 1:
                newline_pos = str.rfind(self.buf, "\n")
                # print(newline_pos)
                pos = self.file.tell()
                if newline_pos != -1:
                    # Found a newline
                    line = self.buf[newline_pos + 1 :]
                    self.buf = self.buf[:newline_pos]
                    if pos != 0 or newline_pos != 0 or self.trailing_newline:
                        line += "\n"
                    yield line
                else:
                    if pos == 0:
                        # Start-of-file
                        return ""
                    else:
                        # Need to fill buffer
                        toread = min(self.BLKSIZE, pos)
                        self.file.seek(-toread, 1)
                        self.buf = self.file.read(toread).decode("UTF-8") + self.buf
                        self.file.seek(-toread, 1)
                        if pos - toread == 0:
                            self.buf = "\n" + self.buf

    def readFiles(self, files):
        f=None
        for file in files:
            f0=open(file,"r")
            lineCount=len(f0.readlines())
            f0.close()
            f = open(file, "rb")
            br = self.BackwardsReader(f)

            for i in range(lineCount):
                yield br.readline()
        f.close()




