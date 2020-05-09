# Imports
import chardet
import os
import re
import subprocess
from pathlib import Path
from unidecode import unidecode

import digiformatter as df

# Constants
herepath = os.path.dirname(os.path.abspath(__file__))


def iniparse(ini, key, default=None):
    regex = re.compile(r"^([^\s=]+)\s*=\s*(.+)$")
    tag_regex = re.compile(r"<[^>]*>")

    with open(ini, "rb") as f:
        input_bytes = f.read()
        encoding = chardet.detect(input_bytes)["encoding"]

    with open(ini, "r", encoding = encoding) as f:
        for line in f:
            match = regex.match(line.strip())
            if not match:
                continue
            linekey, value = match.groups()
            if key != linekey:
                continue
            value = tag_regex.sub("", value)
            return unidecode(value)
    return default


# Remove prefix function.
def remove_prefix(s, prefix):
    if s.startswith(prefix):
        return s[len(prefix):].strip()
    else:
        return s.strip()


# Setup functions
def choosepaths():
    CHfolder = ""
    destfolder = ""
    CHfolder = input("Please type the full path of your input directory.\n>")
    CHfolder = CHfolder.replace("/", "\\")
    destfolder = input("Please type the full path of your output directory.\n>")
    destfolder = destfolder.replace("/", "\\")
    if CHfolder == "":
        CHfolder = "F:\\chs"
    if destfolder == "":
        destfolder = "F:\\ch2mp3"
    confirm = input(f"Input folder: {CHfolder}\nOutput folder: {destfolder}\nAre you sure about this? Type \"Y\" or \"N\".\n>")
    if confirm.lower() == 'y':
        CHfolder = Path(CHfolder)
        destfolder = Path(destfolder)
        return CHfolder, destfolder
    else:
        return choosepaths()


def convert(relfolder):
    # Setup in and out destinations.
    infolder = os.path.join(CHfolder, relfolder)
    albumart = os.path.join(infolder, "album.png")
    outfolder = os.path.join(destfolder, relfolder)
    outfolder = os.path.split(outfolder)[0]  # Go one folder up.

    # Name the outfile.
    outfile = os.path.join(outfolder, Path(infolder.rpartition('\\')[2] + ".mp3"))
    badoutfile = os.path.join(outfolder, Path(infolder.rpartition('\\')[2] + "BAD.mp3"))

    # Temp output.
    # df.msg(f"Converting \"{infolder}\" to \"{outfile}\".")

    # Create the soundlist.
    badsoundlist = []
    p = Path(infolder)
    filelist = list(p.glob('**/*.*'))
    filelist = [str(e) + '\n' for e in filelist]
    for line in filelist:
        newline = line.replace('\\', '/')
        newline = newline.rpartition('/')[2]
        # newline = newline.replace('\u200f', '') # Is this important?
        badsoundlist.append(newline)
    if "crowd.ogg\n" in badsoundlist:
        badsoundlist.remove("crowd.ogg\n")  # F*** crowd noise.

    # Remove all files that aren't sound files.
    soundlist = []
    for item in badsoundlist:
        if item.strip()[-3:] == "ogg" or item.strip()[-3:] == "wav" or item.strip()[-3:] == "mp3":
            soundlist.append(item.strip())

    # How many items are in the list?
    howmany = len(soundlist)
    howmany = str(howmany)

    # Get metadata from .ini.
    ini = f"{infolder}\\song.ini"

    # with open(ini) as file:
    #     print(file.read())

    title = iniparse(ini, "name", "Unknown Title")
    author = album_artist = iniparse(ini, "artist", "Unknown Artist")
    album = iniparse(ini, "album", "Unknown Album")
    year = iniparse(ini, "year", "")
    genre = iniparse(ini, "genre", "Unknown Genre")
    publisher = iniparse(ini, "charter", "Unknown Charter")
    composer = iniparse(ini, "charter", "Unknown Charter")

    # print(f"""title = {title}
    # author = {author}
    # album_artist = {album_artist}
    # year = {year}
    # genre = {genre}
    # comment = {comment}
    # composer = {composer}""")

    df.msg(f"Converting {title} by {author} [{publisher}]")

    # Create the commands.
    command = "ffmpeg/bin/ffmpeg.exe -hide_banner -loglevel quiet"  # Execute ffmpeg.
    for soundfile in soundlist:
        command += f" -i \"{infolder}\\{soundfile}\""  # Add all the sound files as inputs.
    command += f" -filter_complex \"amix=inputs={howmany}\""  # Mix it all together and you know that it's the best of {howmany} worlds!
    command += f" \"{badoutfile}\""  # Output the mixed recording to the output file.

    command2 = f"ffmpeg/bin/ffmpeg.exe -hide_banner -loglevel quiet -i \"{badoutfile}\""  # But the output file needs to be filtered again...
    command2 += f" -i \"{albumart}\""
    command2 += f" -map 0:0 -map 1:0"  # (Map the inputs.)
    command2 += f" -filter_complex volume={howmany}.0"  # ...because the result is 1/{howmany}th the volume it should be.
    command2 += f" -id3v2_version 3 -write_id3v1 1"  # Set metadata version.
    command2 += f" -metadata title=\"{title}\""  # Assign metadata tags.
    command2 += f" -metadata author=\"{author}\""
    command2 += f" -metadata artist=\"{author}\""
    command2 += f" -metadata album_artist=\"{album_artist}\""
    command2 += f" -metadata album=\"{album}\""
    command2 += f" -metadata date=\"{year}\""
    command2 += f" -metadata genre=\"{genre}\""
    command2 += f" -metadata publisher=\"{publisher}\""
    command2 += f" -metadata composer=\"{composer}\""
    command2 += f" -metadata:s:v title=\"Album cover\" -metadata:s:v comment=\"Cover (front)\""  # Set the album art.
    command2 += f" \"{outfile}\""  # Replace the old output with the new, louder, tagged one.

    # Execute the command.
    # print(command)
    subprocess.run(command)
    # print(command2)
    subprocess.run(command2)

    # Delete the bad file.
    if os.path.exists(badoutfile):
        os.remove(badoutfile)  # Get rid of the quiet version of the output.


# Make the users client-side song list.
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


# Let's try this:
# Check each folder in the folder list.
# If it has a folder in it self, it's not a dead end so don't add it to the list.
# Otherwise do.
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
        if deadendbool is True:
            deadends.append(folder)
    for line in deadends:
        printdeadends.append(line + "\n")
    with open('clientdeadends.txt', 'w+', encoding="utf-8") as f:
        f.writelines(printdeadends)
    return deadends


# Make the folders for the files if they aren't there, since open() can't make subfolders.
def makeFolderStruct():
    for folder in CHlist:
        folder = os.path.split(folder)[0]
        try:
            os.makedirs(os.path.join(destfolder, folder))
        except FileExistsError:
            # Folder's already there. Don't gotta make it again.
            pass


# Main code.
CHfolder, destfolder = choosepaths()
df.msg("Making file list...")
CHlist = makeFileList()
df.msg("Making folders...")
makeFolderStruct()
print("Begin conversion.")
for item in getdeadends(CHlist):
    convert(item)
