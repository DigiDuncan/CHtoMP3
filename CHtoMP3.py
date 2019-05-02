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

#Setup functions
def choosepaths():
	global CHfolder
	global destfolder
	CHfolder = input("Please type the full path of your input directory.\n>")
	CHfolder = CHfolder.replace("\\", "/")
	destfolder = input("Please type the full path of your output directory.\n>")
	destfolder = destfolder.replace("\\", "/")
	if CHfolder == "test": CHfolder = "F:/chs"
	if destfolder == "test": destfolder = "F:/CHtoMP3 Songs"
	confirm = input("Input folder: {0}\nOutput folder: {1}\nAre you sure about this? Type \"Y\" or \"N\".\n>".format(CHfolder, destfolder))
	if confirm.lower() == 'y':
		return
	else:
		choosepaths()

def convert(relfolder):
	global CHfolder
	global destfolder
	global herepath

	#Setup in and out destinations.
	infolder = CHfolder + relfolder
	outfolder = destfolder + relfolder
	outfolder = os.path.split(outfolder)[0]

	#Name the outfile.
	outfile = outfolder + "/" + infolder.rpartition('/')[2] + ".mp3"
	badoutfile = outfolder + "/" + infolder.rpartition('/')[2] + "BAD.mp3"
	print(f"""OUTFILE CALC:
	outfolder = {outfolder}
	infolder = {infolder}
	infolder.rparttion('/')[2] = {infolder.rpartition('/')[2]}
	outfile = {outfile}
	badoutfile = {badoutfile}""")

	#Create the soundlist.
	badsoundlist = []
	p = Path(infolder)
	filelist = list(p.glob('**/*.*'))
	filelist = [str(e) + '\n' for e in filelist]
	for line in filelist:
		newline = line.replace('\\', '/')
		newline = newline.rpartition('/')[2]
		newline = newline.replace('\u200f', '')
		badsoundlist.append(newline)
	if "crowd.ogg\n" in badsoundlist:
		badsoundlist.remove("crowd.ogg\n")

	print(f"badsoundlist: {badsoundlist}")

	#Remove all files that aren't sound files.
	soundlist = []
	for item in badsoundlist:
		if item.strip()[-3:] == "ogg" or item.strip()[-3:] == "wav" or item.strip()[-3:] == "mp3":
			soundlist.append(item.strip())

	print(f"soundlist: {soundlist}")

	#How many items are in the list?
	howmany = len(soundlist)
	howmany = str(howmany)

	print(f"howmany: {howmany}")

	#Create the command.
	command = "ffmpeg -hide_banner -loglevel quiet" #Execute ffmpeg without output on screen.
	for soundfile in soundlist:
		command += f" -i \"{infolder + '/' + soundfile}\"" #Add all the sound files as inputs.
	command += f" -filter_complex \"amix=inputs={howmany}\"" #Mix it all together and you know that it's the best of {howmany} worlds!
	command += f" \"{badoutfile}\"" #Output the mixed recording to the output file.
	command += f" && ffmpeg -hide_banner -loglevel quiet -i \"{badoutfile}\"" #But the output file needs to be filtered again...
	command += f" -filter_complex volume={howmany}.0" #...because the result is 1/{howmany}th the volume it should be.
	command += f" \"{outfile}\"" #Replace the old output with the new, louder one.

	print(f"command: {command}")

	#Execute the command.
	os.system(f"cd {herepath}")
	os.system("cd ffmpeg/bin")
	os.system(command)

	#Delete the bad file.
	if os.path.exists(badoutfile): os.remove(badoutfile) #Get rid of the quiet version of the output.

#Make the users client-side song list.
def makeFileList():
	global CHlist
	p = Path(CHfolder)
	filelist = list(p.glob('**/*.*'))
	filelist = [str(e) + '\n' for e in filelist]
	for line in filelist:
		if os.path.isdir(line.strip()):
			newline = line.replace('\\', '/')
			newline = newline.replace(CHfolder, '')
			newline = newline.replace('\u200f', '')
			CHlist.append(newline)
	with open('clientfolderlist.txt', 'w+', encoding="utf-8") as f:
		f.writelines(CHlist)

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
	for item in CHlist:
		folder = item.strip()
		folder = os.path.split(folder)[0]
		try:
			os.makedirs(destfolder + folder)
		except FileExistsError:
			#Folder's already there. Don't gotta make it again.
			pass

#Main code.
choosepaths()
print(herepath)
makeFileList()
makeFolderStruct()
for item in CHlist:
	convert(item.strip())
