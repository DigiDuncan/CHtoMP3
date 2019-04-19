from colored import fore, back, style, fg, bg, attr
from time import strftime, localtime
import math
from DPNVT import *

def load(message):
	print((fg(238) + message + style.RESET))
def time():
	return((fore.MAGENTA + strftime("%d %b %H:%M:%S | ", localtime()) + style.RESET))
def warn(message):
	print((time() + fore.YELLOW + message + style.RESET))
def crit(message):
	print((time() + back.RED + style.BOLD + message + style.RESET))
def test(message):
	print((time() + fore.BLUE + message + style.RESET))
def msg(message):
	print((time() + fg(51) + message + style.RESET))
def splash(message):
	print(fore.YELLOW + style.UNDERLINED + message + style.RESET)

ascii = r"""
                                                                                   .---.
████████▄     ▄███████▄ ███▄▄▄▄      ▄████████ ▄██   ▄   ███▄▄▄▄    ▄████████     @ @   )    ┌{1}┐
███   ▀███   ███    ███ ███▀▀▀██▄   ███    ███ ███   ██▄ ███▀▀▀██▄ ███    ███     ^     |   <│{0}!│
███    ███   ███    ███ ███   ███   ███    █▀  ███▄▄▄███ ███   ███ ███    █▀     [|]    | ## └{1}┘
███    ███   ███    ███ ███   ███   ███        ▀▀▀▀▀▀███ ███   ███ ███           /      |####
███    ███ ▀█████████▀  ███   ███ ▀███████████ ▄██   ███ ███   ███ ███          (       |####
███    ███   ███        ███   ███          ███ ███   ███ ███   ███ ███    █▄     \| /   |####
███   ▄███   ███        ███   ███    ▄█    ███ ███   ███ ███   ███ ███    ███   / |.'   |###
████████▀   ▄████▀       ▀█   █▀   ▄████████▀   ▀█████▀   ▀█   █▀  ████████▀   _\ ``\   )##
                                       Powered by Project CHOCOLATE           /,,_/,,____#   """

#Create a loading bar. Current resolution: 50c, 1c/2.5p.
def createloadbar(c, t):
	progress = ((c/t)*100)
	bar = ""
	percentage = progress
	progress *= 2
	progress = int(progress)
	bars = math.floor(progress/4)
	bar = FULL * bars
	shade = progress - (bars*4)
	if shade == 1: bar += TWENTYFIVE
	if shade == 2: bar += FIFTY
	if shade == 3: bar += SEVENTYFIVE
	printableperc = int((c/t)*10000) / 100
	return "{0} {1}%".format(bar, printableperc)

def getprintitem(item):
	if len(item) > 80:
		printitem = "..." + item[-80:]
	else:
		printitem = item
	return printitem
