from pathlib import Path
import os

infolder = ""
outfolder = ""
outfile = ""
badoutfile = ""

#Setup functions
def choosepaths():
	global infolder
	global outfolder
	infolder = input("Please type the full path of your input directory.\n>")
	infolder = infolder.replace("\\", "/")
	outfolder = input("Please type the full path of your output directory.\n>")
	outfolder = outfolder.replace("\\", "/")
	if infolder == "test": infolder = "C:/chs/02 Official RB Games/1 Rock Band 1/Rock Band 1 Base Game/Tier 1 [RB1]/01.1 OK Go - Here It Goes Again"
	if outfolder == "test": outfolder = "C:/Users/digid/Desktop"
	confirm = input("Input folder: {0}\nOutput folder: {1}\nAre you sure about this? Type \"Y\" or \"N\".\n>".format(infolder, outfolder))
	if confirm.lower() == 'y':
		return
	else:
		choosepaths()

def nameoutfile():
	global outfile
	global badoutfile
	outfile = outfolder + "/" + infolder.rpartition('/')[2] + ".mp3"
	badoutfile = outfolder + "/" + infolder.rpartition('/')[2] + "BAD.mp3"
	print(f"""OUTFILE CALC:
	outfolder = {outfolder}
	infolder = {infolder}
	infolder.rparttion('/')[2] = {infolder.rpartition('/')[2]}
	outfile = {outfile}
	badoutfile = {badoutfile}""")

def convert(infolder, outfile):
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
	if "crowd.ogg" in badsoundlist:
		badsoundlist.remove("crowd.ogg")

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
	command = "ffmpeg"
	for soundfile in soundlist:
		command += f" -i \"{infolder + '/' + soundfile}\"" #Add all the sound files as inputs.
	command += f" -filter_complex \"amix=inputs={howmany}\"" #Mix it all together and you know that it's the best of {howmany} worlds!
	command += f" \"{badoutfile}\"" #Output the mixed recording to the output file.
	command += f" && ffmpeg -i \"{badoutfile}\"" #But the output file needs to be filtered again...
	command += f" -filter_complex volume={howmany}.0" #...because the result is 1/{howmany}th the volume it should be.
	command += f" \"{outfile}\"" #Overwrite the old output with the new, louder one.

	print(f"command: {command}")

	#Execute the command.
	os.system("cd ffmpeg/bin")
	os.system(command)

	#Delete the bad file.
	if os.path.exists(badoutfile): os.remove(badoutfile)

#Main program.
choosepaths()
nameoutfile()
convert(infolder, outfile)
