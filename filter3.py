#filter3: channel10 的音符是否都在35-81之间
from mido import Message, MidiFile, MidiTrack

import py_midicsv as pm
status = "111"

def filter3(status,filename):
    mid = MidiFile('feeling.mid')
    note_on_chan10 = []
    flag = ""

    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            print(msg)
            try:
                if msg.channel == 9:
                    note_on_chan10.append(msg)
            except:
                continue

    for msg in note_on_chan10:
        try:
            if msg.note < 35 or msg.note > 81:
                print(msg.note)
                flag = 'not-GM'
                break
        except:
            continue

    if flag == 'not-GM':
        status += '0'
    else:
        status += '1'

    print(status)
    return status