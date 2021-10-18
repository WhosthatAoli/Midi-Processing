#filter1：判断是否通过解析

from mido import Message, MidiFile, MidiTrack
import py_midicsv as pm

def filter1(status,filename):
    try:
        mid = MidiFile("{}".format(filename))    #mido解析
        status += '1'
    except:
        status += "0"
        pass

    try:
        csv_string = pm.midi_to_csv("{}".format(filename))     #midicsv解析
        status += '1'
    except:
        status += "0"
        pass

    print(status)
    return status




status = ""
filename = "fly away.mid"
filter1(status,filename)



