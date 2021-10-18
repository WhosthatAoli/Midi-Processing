#filter4: 判断是否有其它channel的音符在35-81之间
from mido import Message, MidiFile, MidiTrack
status = "110"

def filter4(status, filename):
    mid = MidiFile('feeling.mid')
    maybe = []
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        result = True
        for msg in track:
            print(msg)
            try:
                if msg.note < 35 or msg.note > 81:
                    result = False
                    #print('oob')
                    break    #下一个track
            except:
                continue
        if result:
            maybe.append(i)
    print(maybe)
    if len(maybe) > 0:
        status += '1'
    else:
        status += '0'

    print(status)
    return status