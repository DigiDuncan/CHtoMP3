#Imports
from DPNVT import *
from DPNGourmet import *
import os
from pathlib import Path
import re
import subprocess
import configparser

#Constants
herepath = os.path.dirname(os.path.abspath(__file__))

#Remove prefix function.
def remove_prefix(s, prefix):
     if s.startswith(prefix):
         return s[len(prefix):].strip()
     else:
         return s.strip()

def insert_section(file):
    yield "[CH]\n"
    yield from file

#Setup functions
def choosepaths():
    CHfolder = ""
    destfolder = ""
    CHfolder = input("Please type the full path of your input directory.\n>")
    CHfolder = CHfolder.replace("/", "\\")
    destfolder = input("Please type the full path of your output directory.\n>")
    destfolder = destfolder.replace("/", "\\")
    if CHfolder == "test": CHfolder = "F:\\chs"
    if destfolder == "test": destfolder = "F:\\CHtoMP3 Songs"
    if CHfolder == "test2": CHfolder = "C:\\chs"
    if destfolder == "test2": destfolder = "C:\\CHtoMP3 Songs"
    confirm = input(f"Input folder: {CHfolder}\nOutput folder: {destfolder}\nAre you sure about this? Type \"Y\" or \"N\".\n>")
    if confirm.lower() == 'y':
        CHfolder = Path(CHfolder)
        destfolder = Path(destfolder)
        return CHfolder, destfolder
    else:
        return choosepaths()

def convert(relfolder):
    #Setup in and out destinations.
    infolder = os.path.join(CHfolder, relfolder)
    outfolder = os.path.join(destfolder, relfolder)
    outfolder = os.path.split(outfolder)[0] #Go one folder up.

    #Name the outfile.
    outfile = os.path.join(outfolder, Path(infolder.rpartition('\\')[2] + ".mp3"))
    badoutfile = os.path.join(outfolder, Path(infolder.rpartition('\\')[2] + "BAD.mp3"))

    #Temp output.
    print(f"Converting \"{infolder}\" to \"{outfile}\".")

    #Create the soundlist.
    badsoundlist = []
    p = Path(infolder)
    filelist = list(p.glob('**/*.*'))
    filelist = [str(e) + '\n' for e in filelist]
    for line in filelist:
        newline = line.replace('\\', '/')
        newline = newline.rpartition('/')[2]
        #newline = newline.replace('\u200f', '') #Is this important?
        badsoundlist.append(newline)
    if "crowd.ogg\n" in badsoundlist:
        badsoundlist.remove("crowd.ogg\n") #F*** crowd noise.

    #Remove all files that aren't sound files.
    soundlist = []
    for item in badsoundlist:
        if item.strip()[-3:] == "ogg" or item.strip()[-3:] == "wav" or item.strip()[-3:] == "mp3":
            soundlist.append(item.strip())

    #How many items are in the list?
    howmany = len(soundlist)
    howmany = str(howmany)

    #Make a config parser.
    config = configparser.ConfigParser()

    #Get metadata from .ini.
    with open(f"{infolder}\\song.ini") as ini:
        config.read_file(ini)
    songini = config["song"]
    title = songini.get("name", "Unknown Title")
    author = album_artist = songini.get("artist", "Unknown Artist")
    album = songini.get("album", "Unknown Album")
    year = songini.get("year", "")
    genre = songini.get("genre", "Unknown Genre")
    comment = songini.get("charter", "Unknown Charter")
    comment = "charted by " + comment
    composer = songini.get("charter", "Unknown Charter")

    print(f"""title = {title}
author = {author}
album_artist = {album_artist}
year = {year}
genre = {genre}
comment = {comment}
composer = {composer}""")

    #Create the commands.
    command = "ffmpeg/bin/ffmpeg.exe -hide_banner -loglevel quiet" #Execute ffmpeg.
    for soundfile in soundlist:
        command += f" -i \"{infolder}\\{soundfile}\"" #Add all the sound files as inputs.
    command += f" -filter_complex \"amix=inputs={howmany}\"" #Mix it all together and you know that it's the best of {howmany} worlds!
    command += f" \"{badoutfile}\"" #Output the mixed recording to the output file.

    command2 = f"ffmpeg/bin/ffmpeg.exe -hide_banner -loglevel quiet -i \"{badoutfile}\"" #But the output file needs to be filtered again...
    command2 += f" -filter_complex volume={howmany}.0" #...because the result is 1/{howmany}th the volume it should be.
    command2 += f" -metadata title=\"{title}\""
    command2 += f" -metadata author=\"{author}\""
    command2 += f" -metadata artist=\"{author}\""
    command2 += f" -metadata album_artist=\"{album_artist}\""
    command2 += f" -metadata album=\"{album}\""
    command2 += f" -metadata year=\"{year}\""
    command2 += f" -metadata genre=\"{genre}\""
    command2 += f" -metadata comment=\"{comment}\""
    command2 += f" -metadata composer=\"{composer}\"" #Assign metadata tags.
    command2 += f" \"{outfile}\"" #Replace the old output with the new, louder, tagged one.

    #Execute the command.
    #subprocess.run(f"cd {herepath}")
    #subprocess.run("cd ffmpeg/bin")
    print(command)
    subprocess.run(command)
    print(command2)
    subprocess.run(command2)

    #Delete the bad file.
    if os.path.exists(badoutfile): os.remove(badoutfile) #Get rid of the quiet version of the output.

#Make the users client-side song list.
def makeFileList():
    printlist = []
    CHlist = []
    p = Path(CHfolder)
    filelist = list(p.glob('**/*'))
    for line in filelist:
        if os.path.isdir(line):
            newline = os.path.relpath(line, CHfolder)
            CHlist.append(newline)
    for line in CHlist:
        printlist.append(line + "\n")
    with open('clientfolderlist.txt', 'w+', encoding="utf-8") as f:
        f.writelines(printlist)
    return CHlist

#Let's try this:
#Check each folder in the folder list.
#If it has a folder in it self, it's not a dead end so don't add it to the list.
#Otherwise do.
def getdeadends(CHlist):
    printdeadends = []
    deadends = []
    for folder in CHlist:
        p = Path(os.path.join(CHfolder, folder))
        sublist = p.iterdir()
        deadendbool = True
        for item in sublist:
            if item.is_dir():
                deadendbool = False
                break
        if deadendbool == True: deadends.append(folder)
    deadends.remove("Game Icons (Dont Put In Songs)")
    deadends.remove("Highways (Dont Put In Songs)")
    for line in deadends:
        printdeadends.append(line + "\n")
    with open('clientdeadends.txt', 'w+', encoding="utf-8") as f:
        f.writelines(printdeadends)
    return deadends


#Make the folders for the files if they aren't there, since open() can't make subfolders.
def makeFolderStruct():
    for folder in CHlist:
        folder = os.path.split(folder)[0]
        try:
            os.makedirs(os.path.join(destfolder, folder))
        except FileExistsError:
            #Folder's already there. Don't gotta make it again.
            pass

#Main code.
CHfolder, destfolder = choosepaths()
print("Making file list.")
CHlist = makeFileList()
print("Making folders.")
makeFolderStruct()
print("Begin conversion.")
for item in getdeadends(CHlist):
    convert(item)
