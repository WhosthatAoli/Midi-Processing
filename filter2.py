#filter2: 判断是否有channel 10，使用midi来解析

from mido import Message, MidiFile, MidiTrack
import py_midicsv as pm
status = "11"

def filter2(status,filename):
    mid = MidiFile('feeling.mid')
    note_on_chan10 = []
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            print(msg)
            try:
                if msg.channel == 9:
                    note_on_chan10.append(msg)
            except:
                continue

    print(len(note_on_chan10))
    print(note_on_chan10)
    if len(note_on_chan10) > 0 :
        status += '1'
    else:
        status += '0'

    print(status)



