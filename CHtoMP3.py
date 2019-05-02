#Imports
from DPNVT import *
from DPNGourmet import *
import os

#Variables
CHfolder = ""
outfolder = ""
CHlist = []
deadends = []

#Constants
herepath = os.path.dirname(os.path.abspath(__file__))

#Make the users client-side song list.
def makeFileList():
	global CHlist
	p = Path(CHfolder)
	filelist = list(p.glob('**/*.*'))
	filelist = [str(e) + '\n' for e in filelist]
	for line in filelist:
		newline = line.replace('\\', '/')
		newline = newline.replace(CHfolder, '')
		newline = newline.replace('\u200f', '')
		CHlist.append(newline)
	with open('clientfilelist.txt', 'w+', encoding="utf-8") as f:
		f.writelines(CHlist)

def convert(infile, outfile):
	os.sys("cd .")
	os.sys("cd ffmpeg/bin")
	os.sys("ffmpeg {0} {1}") #This won't work.

def isAFile(fileloc):
	isafile = r'\/.*\.\w{2,8}$'
	if bool(re.search(isafile, fileloc)):
		return True
	else:
		return False

def isAFolder(fileloc):
	#Here's to hoping the only two things that can be in a Windows path are files and folders.
	isafile = r'\/.*\.\w{2,8}$'
	if bool(re.search(isafile, fileloc)):
		return False
	else:
		return True

#Setup functions
def choosepaths():
	global CHfolder
	global outfolder
	CHfolder = input("Please type the full path of your Clone Hero Songs directory.\n>")
	CHfoldler = CHfolder.replace("\\", "/")
	outfolder = input("Please type the full path of your output directory.\n>")
	outfolder = outfolder.replace("\\", "/")
	if CHfolder == "test": CHfolder = "E:/chs"
	if outfolder == "test": outfolder = "E:/CHtoMP3 Songs"
	confirm = input("Input folder: {0}\nOutput folder: {1}\nAre you sure about this? Type \"Y\" or \"N\".\n>".format(CHfolder, outfolder))
	if confirm.lower() == 'y':
		return
	else:
		choosepaths()

#Let's try this:
#Check each folder in the folder list.
#If it has a folder in it self, it's not a dead end so don't add it to the list.
#Otherwise do.
#Returns a list.
def getdeadends():
	pass

#Make the folders for the files if they aren't there, since open() can't make subfolders.
def makeFolderStruct():
	msg("Making file structure...")
	#Placeholder text, may or may not be overwritten.
	load("No folders to make.")
	for item in CHlist:
		#[::-1] is slice syntax for reversing a string.
		folder = item[::-1]
		folder = re.sub(r'.*?\/', '', folder, 1)
		folder = folder[::-1]
		printfolder = getprintitem(folder)
		try:
			os.makedirs(outfolder + folder)
			print(OverwriteLines(1) + 'Created folder {0}'.format(printfolder))
		except FileExistsError:
			#Folder's already there. Don't gotta make it again.
			pass
	for folder in CHlist:
		if isAFolder(item):
			printfolder = getprintitem(folder)
			try:
				os.makedirs(outfolder + folder)
				print(OverwriteLines(1) + 'Created folder {0}'.format(printfolder))
			except FileExistsError:
				#Folder's already there. Don't gotta make it again.
				pass

#Main code.
