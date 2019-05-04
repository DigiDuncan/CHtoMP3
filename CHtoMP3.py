#Imports
from DPNVT import *
from DPNGourmet import *
import os
from pathlib import Path
import re


#Variables
CHfolder = ""
destfolder = ""
CHlist = []
deadends = []

#Constants
herepath = os.path.dirname(os.path.abspath(__file__))

#Remove prefix function.
def remove_prefix(s, prefix):
    return s[len(prefix):] if s.startswith(prefix) else s

#Setup functions
def choosepaths():
	global CHfolder
	global destfolder
	CHfolder = input("Please type the full path of your input directory.\n>")
	CHfolder = CHfolder.replace("/", "\\")
	destfolder = input("Please type the full path of your output directory.\n>")
	destfolder = destfolder.replace("/", "\\")
	if CHfolder == "test": CHfolder = "F:\\chs"
	if destfolder == "test": destfolder = "F:\\CHtoMP3 Songs"
	if CHfolder == "test2": CHfolder = "C:\\chs"
	if destfolder == "test2": destfolder = "C:\\CHtoMP3 Songs"
	confirm = input("Input folder: {0}\nOutput folder: {1}\nAre you sure about this? Type \"Y\" or \"N\".\n>".format(CHfolder, destfolder))
	if confirm.lower() == 'y':
		Path(CHfolder)
		Path(destfolder)
		return
	else:
		choosepaths()

def convert(relfolder):
	global CHfolder
	global destfolder
	global herepath

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

	#Set default value for metadata.
	title = "Unknown Title"
	author = "Unknown Artist"
	album_artist = "Unknown Artist"
	album = "Unknown Album"
	year = ""
	genre = "Unknown Genre"
	comment = "charted by Unknown Charter"
	composer = "Unknown Charter"

	#Get metadata from .ini.
	ini = open(f"{infolder}\\song.ini", "r")
	for line in ini:
		if line.startswith("name"): title = remove_prefix(line, "name=")
		if line.startswith("artist"): author = remove_prefix(line, "artist=")
		if line.startswith("artist"): album_artist = remove_prefix(line, "artist=")
		if line.startswith("album"): album = remove_prefix(line, "album=")
		if line.startswith("year"): year = remove_prefix(line, "year=")
		if line.startswith("genre"): genre = remove_prefix(line, "genre=")
		if line.startswith("charter"): comment = "charted by " + remove_prefix(line, "charter=")
		if line.startswith("charter"): composer = remove_prefix(line, "charter=")

	#Create the command.
	command = "ffmpeg -hide_banner -loglevel quiet" #Execute ffmpeg without output on screen.
	for soundfile in soundlist:
		command += f" -i \"{infolder + '/' + soundfile}\"" #Add all the sound files as inputs.
	command += f" -filter_complex \"amix=inputs={howmany}\"" #Mix it all together and you know that it's the best of {howmany} worlds!
	command += f" \"{badoutfile}\"" #Output the mixed recording to the output file.
	command += f" && ffmpeg -hide_banner -loglevel quiet -i \"{badoutfile}\"" #But the output file needs to be filtered again...
	command += f" -filter_complex volume={howmany}.0" #...because the result is 1/{howmany}th the volume it should be.
	command += (f" -metadata title={title}"
				f" -metadata author={author}"
				f" -metadata album_artist={album_artist}"
				f" -metadata album={album}"
				f" -metadata year={year}"
				f" -metadata genre={genre}"
				f" -metadata comment={comment}"
				f" -metadata composer={composer}") #Assign metadata tags.
	command += f" \"{outfile}\"" #Replace the old output with the new, louder, tagged one.

	#Execute the command.
	os.system(f"cd {herepath}")
	os.system("cd ffmpeg/bin")
	os.system(command)

	#Delete the bad file.
	if os.path.exists(badoutfile): os.remove(badoutfile) #Get rid of the quiet version of the output.

#Make the users client-side song list.
def makeFileList():
	printlist = []
	global CHlist
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

#Let's try this:
#Check each folder in the folder list.
#If it has a folder in it self, it's not a dead end so don't add it to the list.
#Otherwise do.
#Returns a list.
def getdeadends():
	pass

#Make the folders for the files if they aren't there, since open() can't make subfolders.
def makeFolderStruct():
	global destfolder
	for folder in CHlist:
		folder = os.path.split(folder)[0]
		try:
			os.makedirs(os.path.join(destfolder, folder))
		except FileExistsError:
			#Folder's already there. Don't gotta make it again.
			pass

#Main code.
choosepaths()
print(herepath)
print("Making file list.")
makeFileList()
print("Making folders.")
makeFolderStruct()
print("Begin conversion.")
for item in CHlist:
	convert(item)
