import os
import shutil
import random
import time 	# For optional use in displaying match results in "real time" - Place time.sleep(n) between rounds where 'n' is a customisable delay in seconds.
import json
import readline
import pathlib
#Playing around with the idea of including sounds. It was successful, but commenting out to concentrate on functionality before fine-tuning.
#import playsound
#playsound.playsound(str(pathlib.Path(__file__).parent.resolve())+'/intro.wav',False)
#time.sleep(4)
homepath = str(pathlib.Path(__file__).parent.resolve())+"/"
for i in range(10):
	print("\033[0;37;40m")
alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','V','Z']
# DISPLAY ASCII ART FROM emstitle FILE WITH RULES FOR APPLYING COLOUR.
with open(homepath+"emstitle","r") as emstitle:
	for line in emstitle:
		printline = ""
		for char in line.rstrip("\n"):
			if char.upper() in alpha:
				printline +=  "\033[0;34;40m"+char
			elif char == "#":
				printline += "\033[0;35;40m"+char
			else:
				printline += "\033[0;33;40m"+char
		print(printline)
#time.sleep(3)
print("\033[0;37;40m") # adds a new line between art and menu, resets fortmatting to no italic/bold/underling;white text;black background [NOTE: avoid using tabs in prints as these seem to reset formatting to terminal defaults and could clash)
def menu():
	print("          MAIN  MENU          ")
	print("==============================")
	print("       \033[4;37;40mASSET MANAGEMENT\033[0;37;40m")
	print(" 1) Create A Wrestler")
	print(" 2) Review/Edit A Wrestler")
	print(" 3) Create A Move Set")
	print(" 4) Review/Edit A Move Set")
	print("           \033[4;37;40mBOOKING\033[0;37;40m")
	print(" 5) Book A Match")
	print(" 6) Book An Event")
	print("           \033[4;37;40mOTHER\033[0;37;40m")
	print(" X) Exit")
	print("")
	#time.sleep(1)
	while True:
		response =input("\033[0;34;40mPlease select an option: \033[0;37;40m")
		try:
			if response.upper() == "X":
				os._exit(os.EX_OK)
			elif response == "1":
				caw(input("Please enter the name of this wreslter: "))
			elif response == "2":
				list_wrestlers = os.listdir(homepath+"wrestlers/")
				print("PLEASE CHOOSE FROM BELOW")
				print("========================")
				for wrestler in list_wrestlers:
					if wrestler != "movelists":
						print(wrestler)
				print("")
				openfile = input("Please enter filename exactly as it appears above ('X' to quit.): ")
				try:
					opentemplate("wrestlers/"+openfile)
				except:
					print("Error opening wrestler file " +openfile+"\nERROR CODE 001")
			elif response == "3":
				createmoves("wrestlers/movelists/"+input("Please enter the \033[0;34;40mname\033[0;37;40m of the \033[0;34;40mmoveslist\033[0;37;40m you want to create: ")+".emsm")
			elif response == "4":
				list_moves = os.listdir(homepath+"wrestlers/movelists/")
				print("PLEASE CHOOSE FROM BELOW")
				print("========================")
				for move in list_moves:
					print(move)
				print("")
				openfile = input("Please enter filename exactly as it appears above ('X' to quit.): ")
				try:
					openmoves("wrestlers/movelists/"+openfile)
				except:
					print("Error opening moveslist file " +openfile+"\nERROR CODE 002")
			elif int(response) in range(5,7):
				print("\033[1;31;40mThis option is unavailable right now. Please choose another.\033[0;37;40m")
			else:
				print("\033[1;31;40mPlease choose a valid option (1-6).\033[0;37;40m")
		except:
			print("\033[1;31;40mPlease choose a valid option. 1-6 or X to exit.\033[0;37;40m")
# SAVE MOVESLIST FILE (CAW/WRESTLER EDIT ONLY)
def savemoves(movesfile):
	try:
		with open(homepath+"wrestlers/movelists/"+movesfile) as f:
			print("wrestlers/movelists/"+movesfile+" exists.")
	except IOError:
		print("wrestlers/movelists/"+movesfile+" does not exist. Creating file.")
		shutil.copyfile(homepath+"wrestlers/movelists/template.emsm", homepath+"wrestlers/movelists/"+movesfile)
		print("wrestlers/movelists/"+movesfile+" created.")
# CREATE-A-WRESTLER
def caw(savefile):
	print("\n\033[4;32;40m\033[1;32;40mFLAGS\033[0;37;40m\nWhen you are asked to enter decriptions for a move, you can enter flags in the text that will automatically be replaced in the match sim by the relevant data.\n\033[0;35;40m{att}\033[0;37;40m and \033[0;35;40m{def}\033[0;37;40m will use one of the names relating to the attacker or defender respectively.\nYou can insert he/his/him after att or def in the flag to get the relevant pronoun for the wrestler concerned.\n\033[0;35;40m(e.g. {att} kicks {def} in the gut. {defhe} didn't is clutching {defhis} stomach. Look at {att}! {atthe} looks pleased with {atthim}self.\033[0;37;40m\n")
	filetemplate = {}
	with open(homepath+"wrestlers/template.emsw", "r") as read:
		filetemplate = json.load(read)
	for i in filetemplate:
		filetemplate[i] = None
	for i in filetemplate:
		if "[LIST]" in i:
			templist = []
			while True:
				ans = input("Leave blank when done.\n\033[0;34;40m"+i.replace("[LIST]","") +"\033[0;37;40m : ")
				if ans.upper() == "!EXIT":
					menu()
				elif ans == "":
					break
				else:
					templist.append(ans)
			filetemplate[i] = templist
		elif "[4-15]" in i:
			while True:
				ans = input("\033[0;34;40m"+i+"\033[0;37;40m : ")
				if int(ans) in range(4,16):
					filetemplate[i] = ans
					break
				else:
					print("Please enter a valid figure.")
		elif "[MAX 20]" in i:
			while True:
				ans = input("\033[0;34;40m"+i+"\033[0;37;40m : ")
				if int(ans) in range(1,21):
					filetemplate[i] = ans
					break
				else:
					print("Please enter a valid figure.")
		elif "[MAX 10]" in i:
			while True:
				ans = input("\033[0;34;40m"+i+"\033[0;37;40m : ")
				if int(ans) in range(1,11):
					filetemplate[i] = ans
					break
				else:
					print("Please enter a valid figure.")
		elif "[MAX 120]" in i:
			while True:
				ans = input("\033[0;34;40m"+i+"\033[0;37;40m : ")
				if int(ans) in range(1,121):
					filetemplate[i] = ans
					break
				else:
					print("Please enter a valid figure.")
		else:
			ans = input("\033[0;34;40m"+i+"\033[0;37;40m : ")
			filetemplate[i] = ans
	try:
		savemoves(filetemplate["MOVESLIST FILE (if file does not exist, one will be created)"])
	except:
		print("error saving moveslist")
	with open(homepath+"wrestlers/"+savefile+".emsw", "w") as save:
		json.dump(filetemplate, save)
	print("Wreslter file saved to wrestlers/"+savefile+".emsw\nReturning to menu...")
	menu()
# REVIEW/EDIT WRESTLERS
def opentemplate(openfile):
	print("\n\033[4;32;40m\033[1;32;40mFLAGS\033[0;37;40m\nWhen you are asked to enter decriptions for a move, you can enter flags in the text that will automatically be replaced in the match sim by the relevant data.\n\033[0;35;40m{att}\033[0;37;40m and \033[0;35;40m{def}\033[0;37;40m will use one of the names relating to the attacker or defender respectively.\nYou can insert he/his/him after att or def in the flag to get the relevant pronoun for the wrestler concerned.\n\033[0;35;40m(e.g. {att} kicks {def} in the gut. {defhe} didn't is clutching {defhis} stomach. Look at {att}! {atthe} looks pleased with {atthim}self.\033[0;37;40m\n")
	filetemplate = {}
	with open(homepath+openfile, "r") as read:
		filetemplate = json.load(read)
	for i in filetemplate:
		if "[LIST]" in i:
			print("\033[0;34;40m"+i+"\033[0;37;40m")
			for c in filetemplate[i]:
				print("\033[0;33;40m"+c+"\033[0;37;40m")
		else:
			print("\033[0;34;40m"+i+"\033[0;37;40m : \033[0;33;40m"+str(filetemplate[i])+"\033[0;37;40m")
		if input("Make changes to \033[0;34;40m"+i+"\033[0;37;40m? [Y/N]: ").upper() == "Y":
			vals = ""
			if "[LIST]" in i:
				print("Leave blank when done")
				vals = []
				while True:
					list_val = input("Enter next value for \033[0;34;40m"+i+"\033[0;37;40m: ")
					if list_val == "":
						break
					else:
						vals.append(list_val)
			else:
				vals = input("Enter value for \033[0;34;40m"+i+"\033[0;37;40m: ")
			filetemplate[i] = vals
			with open(homepath+openfile, "w") as save:
				json.dump(filetemplate, save)
	savemoves(filetemplate["MOVESLIST FILE (if file does not exist, one will be created)"])
	print("Returning to menu...")
	menu()
# REVIEW/EDIT MOVELISTS
def openmoves(openfile):
	print("\n\033[4;32;40m\033[1;32;40mFLAGS\033[0;37;40m\nWhen you are asked to enter decriptions for a move, you can enter flags in the text that will automatically be replaced in the match sim by the relevant data.\n\033[0;35;40m{att}\033[0;37;40m and \033[0;35;40m{def}\033[0;37;40m will use one of the names relating to the attacker or defender respectively.\nYou can insert he/his/him after att or def in the flag to get the relevant pronoun for the wrestler concerned.\n\033[0;35;40m(e.g. {att} kicks {def} in the gut. {defhe} didn't is clutching {defhis} stomach. Look at {att}! {atthe} looks pleased with {atthim}self.\033[0;37;40m\n")
	filetemplate = {}
	poplist = []
	with open(homepath+openfile, "r") as read:
		filetemplate = json.load(read)
	for i in filetemplate:
		print("\033[4;32;40m\033[1;32;40m"+i+"\033[0;37;40m")
		for c in filetemplate[i]:
			if "[LIST]" in c:
				print("\033[0;34;40m"+c+"\033[0;37;40m")
				for d in filetemplate[i][c]:
					print("\033[0;33;40m"+d.replace("{move}",i)+"\033[0;37;40m")
			else:
				print("\033[0;34;40m"+c+"\033[0;37;40m : \033[0;33;40m"+str(filetemplate[i][c])+"\033[0;37;40m")
		response = input("Make changes to \033[0;34;40m"+i+"\033[0;37;40m? [Y/N or D to delete]: ").upper()
		if response == "Y":
			vals = ""
			for c in filetemplate[i]:
				if "[LIST]" in c:
					print("Leave blank when done")
					vals = []
					while True:
						list_val = input("Enter next value for \033[0;34;40m"+c+"\033[0;37;40m: ")
						if list_val == "":
							break
						else:
							vals.append(list_val)
				else:
					vals = input("Enter value for \033[0;34;40m"+c+"\033[0;37;40m: ")
				filetemplate[i][c] = vals
				with open(homepath+openfile, "w") as save:
					json.dump(filetemplate, save)
		elif response == "D":
			poplist.append(i)
	if len(poplist) > 0:
		for popme in poplist:
			filetemplate.pop(popme)
			with open(homepath+openfile, "w") as save:
				json.dump(filetemplate, save)
	print("Returning to menu...")
	menu()
# CREATE MOVESLIST
def createmoves(filename):
	print("\n\033[4;32;40m\033[1;32;40mFLAGS\033[0;37;40m\nWhen you are asked to enter decriptions for a move, you can enter flags in the text that will automatically be replaced in the match sim by the relevant data.\n\033[0;35;40m{att}\033[0;37;40m and \033[0;35;40m{def}\033[0;37;40m will use one of the names relating to the attacker or defender respectively.\nYou can insert he/his/him after att or def in the flag to get the relevant pronoun for the wrestler concerned.\n\033[0;35;40m(e.g. {att} kicks {def} in the gut. {defhe} didn't is clutching {defhis} stomach. Look at {att}! {atthe} looks pleased with {atthim}self.\033[0;37;40m\n\nWhen you're done, leave the answer blank.\n")
	moveslist = {} # The moveslist will be a dictionary of dictionaries, the keys in the moveslist will be the move names. moveslist["movename"] will then hold all the relevant data for that move.
	# Questions below ask for all the data to be stored against each move.
	questions = ["MOVE TYPE [STRIKING/GRAPPLING/AERIAL/SUBMISSION]","IMPACT [4-15]", "WOW! FACTOR [MAX 20]", "SUBMISSION? [Y/N]", "BRIDGE TO PINFALL? [Y/N]", "DESCRIPTION OF SUCCESSFUL EXECUTION OF {move} [LIST]", "DESCRIPTION OF {move} BLOCKED [LIST]", "DESCRIPTION OF {move} REVERSED [LIST]"]
	while True:
		move = input("Enter the \033[0;34;40mname\033[0;37;40m of the next \033[0;34;40mmove\033[0;37;40m: ")
		if move == "":
			break
		elif move == "!exit":
			menu()
		else:
			moveslist[move] = {}
			for question in questions:
				if "[LIST]" in question:
					print ("Leave blank when done.")
					templist = []
					while True:
						ans = input("\033[0;34;40m"+question.replace("{move}",move)+" \033[0;37;40m: ")
						if ans == "":
							break
						else:
							templist.append(ans)
					moveslist[move][question] = templist
				elif "[4-15]" in question:
					while True:
						ans = input("\033[0;34;40m"+question.replace("{move}",move)+" \033[0;37;40m: ")
						if int(ans) in range(4,16):
							moveslist[move][question] = ans
							break
						else:
							print("Please enter a valid figure.")
				elif "[MAX 20]" in question:
					while True:
						ans = input("\033[0;34;40m"+question.replace("{move}",move)+" \033[0;37;40m: ")
						if int(ans) in range(1,21):
							moveslist[move][question] = ans
							break
						else:
							print("Please enter a valid figure.")
				elif "[MAX 10]" in question:
					while True:
						ans = input("\033[0;34;40m"+question.replace("{move}",move)+" \033[0;37;40m: ")
						if int(ans) in range(1,11):
							moveslist[move][question] = ans
							break
						else:
							print("Please enter a valid figure.")
				elif "[MAX 120]" in question:
					while True:
						ans = input("\033[0;34;40m"+question.replace("{move}",move)+" \033[0;37;40m: ")
						if int(ans) in range(1,121):
							moveslist[move][question] = ans
							break
						else:
							print("Please enter a valid figure.")
				else:
					ans = input("\033[0;34;40m"+question.replace("{move}",move)+" \033[0;37;40m: ")
					moveslist[move][question] = ans
	with open(homepath+filename, "w") as save:
		json.dump(moveslist, save)
	print("File saved to "+filename+"\nReturning to menu...")
	menu()
while True:
	menu()
