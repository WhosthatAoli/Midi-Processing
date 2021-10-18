import time
import shutil
timestamp = int(round(time.time() * 1000))
print(timestamp)

def addname(status, filename):
    timestamp = int(round(time.time() * 1000))
    if status == "00":
        addname = "{timestamp}-invalid-{filename}".format(timestamp = timestamp, filename = filename )
        print(addname)
        shutil.copy('datasets/{}'.format(filename), 'Februus/invalid/{addname}'.format(addname = addname))

    if status == "01":
        addname = "{timestamp}-midicsv-{filename}".format(timestamp = timestamp, filename = filename )
        shutil.copy('datasets/{filename}'.format(filename = filename), 'Februus/maybe-gm-valid/{addname}'.format(addname = addname))

    if status == "10":
        addname = "{timestamp}-mido-{filename}".format(timestamp = timestamp, filename = filename )
        shutil.copy('datasets/{filename}'.format(filename = filename), 'Februus/maybe-gm-valid/{addname}'.format(addname = addname))

    if status == "1100" or status == "1110":
        addname = "{timestamp}-oob-{filename}".format(timestamp = timestamp, filename = filename )
        shutil.copy('datasets/{filename}'.format(filename = filename), 'Februus/maybe-not-perc/{addname}'.format(addname = addname))

    if status == "1101":
        addname = "{timestamp}-maybe-perc-{filename}".format(timestamp = timestamp, filename = filename )
        shutil.copy('datasets/{filename}'.format(filename = filename), 'Februus/maybe-perc/{addname}'.format(addname = addname))

    if status == "1111":
        addname = "{timestamp}-gm-valid-perc-{filename}".format(timestamp = timestamp, filename = filename )
        shutil.copy('datasets/{filename}'.format(filename = filename), 'Februus/gm-valid-perc/{addname}'.format(addname = addname))


filename = "feeling.mid"
status = '00'
addname(status,filename)


