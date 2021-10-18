import zipfile,os,time
def zip_ya(start_dir):
    start_dir = start_dir  # 要压缩的文件夹路径
    timestamp = int(round(time.time() * 1000))
    print(timestamp)
    file_news = '{}'.format(timestamp) + "-" + start_dir + '.zip'  # 压缩后文件夹的名字

    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, file_names in os.walk(start_dir):
        f_path = dir_path.replace(start_dir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        f_path = f_path and f_path + os.sep or ''  # 一级文件夹下面的文件，f_path为空了，二级文件夹下面的文件，f_path为二级目录后面加个/
        if len(file_names) == 0 and len(dir_names) == 0:  #空文件夹没有子目录和文件
            z.write(dir_path, f_path)                     #空文件夹的压缩
        for filename in file_names:              #有文件才会复制，忽略空文件夹
            z.write(os.path.join(dir_path, filename), f_path + filename)
    z.close()
    return file_news

zip_ya("Februus")
