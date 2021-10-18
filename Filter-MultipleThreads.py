from mido import Message, MidiFile, MidiTrack
import py_midicsv as pm
import time
import shutil
import os,zipfile
import logging
import threading


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

def readname(filePath):
    filePath = filePath
    name = []
    path = []
    for dir_path, dir_names, file_names in os.walk(filePath):
        f_path = dir_path  # 这一句很重要，不replace的话，就从根目录开始复制,.replace(filePath, '')
        f_path = f_path and f_path + os.sep or ''  # 一级文件夹下面的文件，f_path为空了，二级文件夹下面的文件，f_path为二级目录后面加个/
        for filename in file_names:              #有文件才会复制，忽略空文件夹
            name.append(filename)
            path.append(f_path)
    return name,path

def filter1(status, filename, dataset_path):
    try:
        mid = MidiFile("{}/{}".format(dataset_path,filename))    #mido解析
        status += '1'
    except:
        status += "0"
        pass

    try:
        csv_string = pm.midi_to_csv("{}/{}".format(dataset_path,filename))     #midicsv解析
        status += '1'
    except:
        status += "0"
        pass

    #print(status)
    return status


def filter2(status, mid):
    #mid = MidiFile("{}/{}".format(dataset_path,filename))
    note_on_chan10 = []
    for i, track in enumerate(mid.tracks):
        #print('Track {}: {}'.format(i, track.name))
        for msg in track:
            #print(msg)
            try:
                if msg.channel == 9:
                    note_on_chan10.append(msg)
            except:
                continue

    #print(len(note_on_chan10))
    #print(note_on_chan10)
    if len(note_on_chan10) > 0:
        status += '1'
    else:
        status += '0'

    #print(status)
    return status


def filter3(status, mid):
    #mid = MidiFile("{}/{}".format(dataset_path,filename))
    note_on_chan10 = []
    flag = ""

    for i, track in enumerate(mid.tracks):
        #print('Track {}: {}'.format(i, track.name))
        for msg in track:
            #print(msg)
            try:
                if msg.channel == 9:
                    note_on_chan10.append(msg)
            except:
                continue

    for msg in note_on_chan10:
        try:
            if msg.note < 35 or msg.note > 81:
                #print(msg.note)
                flag = 'not-GM'
                break
        except:
            continue

    if flag == 'not-GM':
        status += '0'
    else:
        status += '1'

    #print(status)
    return status


def filter4(status, mid):
    #mid = MidiFile("{}/{}".format(dataset_path,filename))
    maybe = []
    for i, track in enumerate(mid.tracks):
        #print('Track {}: {}'.format(i, track.name))
        result = True
        for msg in track:
            #print(msg)
            try:
                if msg.note < 35 or msg.note > 81:
                    result = False
                    # print('oob')
                    break  # 下一个track
            except:
                continue
        if result:
            maybe.append(i)
    #print(maybe)
    if len(maybe) > 0:
        status += '1'
    else:
        status += '0'

    #print(status)
    return status


def addname(status, filename, dataset_path):
    timestamp = int(round(time.time() * 1000))
    #print(dataset_path)
    originpath = dataset_path.replace('\\','-')
    originpath = originpath.strip('perc-midi-')   #去掉首目录减少文件名长度
    if len(originpath) > 100:
        originpath = originpath[0:100]
    #originpath = "not set"
    if status == "00":
        addname = "{timestamp}-invalid-'{originpath}'-{filename}".format(timestamp = timestamp, filename = filename, originpath = originpath)
        shutil.copy('{dataset_path}/{filename}'.format(dataset_path = dataset_path, filename = filename), 'Februus/invalid/{addname}'.format(addname = addname))
        #print("copy to invalid")
        logging.info("{filename} from {dataset_path} copy to invalid as {addname}".format(filename = filename, dataset_path = dataset_path, addname = addname))

    if status == "01":
        addname = "{timestamp}-midicsv-'{originpath}'-{filename}".format(timestamp = timestamp, filename = filename , originpath = originpath)
        shutil.copy('{dataset_path}/{filename}'.format(dataset_path = dataset_path, filename = filename), 'Februus/maybe-gm-valid/{addname}'.format(addname = addname))
        #print("copy to maybe-gm-valid")
        logging.info("{filename} from {dataset_path} copy to maybe-gm-valid as {addname}".format(filename = filename, dataset_path = dataset_path, addname = addname))


    if status == "10":
        addname = "{timestamp}-mido-'{originpath}'-{filename}".format(timestamp = timestamp, filename = filename, originpath = originpath )
        shutil.copy('{dataset_path}/{filename}'.format(dataset_path = dataset_path, filename = filename), 'Februus/maybe-gm-valid/{addname}'.format(addname = addname))
        #print("copy to maybe-gm-valid")
        logging.info("{filename} from {dataset_path} copy to maybe-gm-valid as {addname}".format(filename = filename, dataset_path = dataset_path, addname = addname))


    if status == "1100" or status == "1110":
        addname = "{timestamp}-oob-'{originpath}'-{filename}".format(timestamp = timestamp, filename = filename, originpath = originpath )
        shutil.copy('{dataset_path}/{filename}'.format(dataset_path = dataset_path, filename = filename), 'Februus/maybe-not-perc/{addname}'.format(addname = addname))
        #print("copy to maybe-not-perc")
        logging.info("{filename} from {dataset_path} copy to maybe-not-perc as {addname}".format(filename = filename, dataset_path = dataset_path, addname = addname))


    if status == "1101":
        addname = "{timestamp}-maybe-perc-'{originpath}'-{filename}".format(timestamp = timestamp, filename = filename, originpath = originpath )
        shutil.copy('{dataset_path}/{filename}'.format(dataset_path = dataset_path, filename = filename), 'Februus/maybe-perc/{addname}'.format(addname = addname))
        #print("copy to maybe-perc")
        logging.info("{filename} from {dataset_path} copy to maybe-perc as {addname}".format(filename = filename, dataset_path = dataset_path, addname = addname))


    if status == "1111":
        addname = "{timestamp}-gm-valid-perc-'{originpath}'-{filename}".format(timestamp = timestamp, filename = filename, originpath = originpath )
        shutil.copy('{dataset_path}/{filename}'.format(dataset_path = dataset_path, filename = filename), 'Februus/gm-valid-perc/{addname}'.format(addname = addname))
        #print("copy to gm-valid-perc")
        logging.info("{filename} from {dataset_path} copy to gm-valid-perc as {addname}".format(filename = filename, dataset_path = dataset_path, addname = addname))


    return "copy success"

def zip_ya(start_dir):   #空文件夹会被过滤
    start_dir = start_dir  # 要压缩的文件夹路径
    timestamp = int(round(time.time() * 1000))
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

def loop(filenames,filepaths):
    for i in range(len(filenames)):
        status = ""
        filename = filenames[i]
        path = filepaths[i]
        #print(filename)
        status = filter1(status, filename, path)
        if status == "00":
            print("Invalid")
            addname(status, filename, path)  #文件copy

        if status == "10" or status == "01":
            print("Maybe Valid")
            addname(status, filename, path)   #文件copy

        if status == "11":
            mid = MidiFile("{}/{}".format(path, filename))
            status = filter2(status, mid)

            if status == "111":
                status = filter3(status, mid)
                if status == "1110":
                    print("oob")
                    addname(status, filename, path)    #copy
                if status == "1111":
                    print("GM-Valid-Perc")
                    addname(status, filename, path)    #copy

            if status == "110":
                status = filter4(status, mid)
                if status == "1100":
                    print("oob")
                    addname(status, filename, path)    #copy
                if status == "1101":
                    print("Maybe-Perc")
                    addname(status, filename, path)    #copy

##main
if __name__ == "__main__":
    dataset_path = 'perc-midi'      #test data path is here, 'Februus' and its subfolder should be created in the project path
    filenames,filepaths = readname(dataset_path)

    threads = []
    threads_num = 8         #线程数
    per_thread = len(filenames) // threads_num
    print(per_thread)

    for i in range(threads_num):
        if threads_num - i == 1:  # 最后一个线程，分担余下的所有工作量
            t = threading.Thread(target=loop, args=(filenames[i * per_thread:],filepaths[i * per_thread:]))
        else:
            t = threading.Thread(target=loop, args=(filenames[i * per_thread:i * per_thread + per_thread],filepaths[i * per_thread:i * per_thread + per_thread]))
        threads.append(t)
    for i in range(threads_num):
        threads[i].start()
    for i in range(threads_num):  # 等待所有的线程结束
        threads[i].join()

    zip_ya("Februus")