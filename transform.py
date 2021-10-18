from mido import Message, MidiFile, MidiTrack
import shutil
import os

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

def time_signature_check(mid,msg,path,filename):
    if msg.type == 'time_signature':
        if msg.numerator != 4 or msg.denominator != 4:
            copy_to_not4(path,filename)
            print(1)
            return 1
    return 0

def copy_to_not4(dataset_path,filename):
    shutil.copy('{dataset_path}/{filename}'.format(dataset_path=dataset_path, filename=filename),'transform/not4-4/{filename}'.format(filename = filename))


if __name__ == "__main__":
    dataset_path = 'Februus/gm-valid-perc'   #要transform的文件路径
    filenames,filepaths = readname(dataset_path)
    for i in range(len(filenames)):
        filename = filenames[i]
        path = filepaths[i]
        mid = MidiFile("{}/{}".format(path, filename))
        trackNeed = MidiTrack()
        trackNeed.name = 'drum'
        message1 = []
        message2 = []
        flag = int()
        for msg in mid.tracks[0]:
            flag = time_signature_check(mid,msg,path,filename)  #4/4 check
            if flag == 1:
                break                 #退出对track0的扫描
            if msg.type != 'end_of_track':
                message1.append(msg)

        if flag == 1:
            continue                   #退出transform，下一个文件

        for i, track in enumerate(mid.tracks):
            #print('Track {}: {}'.format(i, track.name))
            for msg in track:
                #print(msg)
                try:
                    # mid.type = 0
                    if msg.channel == 9:
                        msg.channel = 0
                        message2.append(msg)
                except:
                    continue

        messageneed = message1 + message2
        for msg in messageneed:
            trackNeed.append(msg)

        #新的midi文件
        mid2 = MidiFile(ticks_per_beat=mid.ticks_per_beat, type=0)    #tpb与老音轨相同,type = 0
        mid2.tracks.append(trackNeed)
        mid2.save('transform/perfect/{}.mid'.format(filename))