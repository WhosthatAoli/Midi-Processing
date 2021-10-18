import os


def readname(filePath):
    filePath = filePath
    name = []
    path = []
    for dir_path, dir_names, file_names in os.walk(filePath):
        f_path = dir_path.replace(filePath, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        f_path = f_path and f_path + os.sep or ''  # 一级文件夹下面的文件，f_path为空了，二级文件夹下面的文件，f_path为二级目录后面加个/
        for filename in file_names:              #有文件才会复制，忽略空文件夹
            name.append(filename)
            path.append(f_path)
    return name,path


if __name__ == "__main__":
    name = readname('datasets')
    print(name)
    for i in name:
        print(i)
