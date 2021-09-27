import pyautogui
from  pynput import keyboard, mouse
import time
import pandas as pd


def myFunction(data, mykeys, l):
	
	index = 0
	
	#pyautogui.moveTo(118,128)N/A

	pyautogui.click(320,486)
	pyautogui.typewrite(str(data[mykeys[index]][0])) #Reference Name 
	index = index+1
	pyautogui.click(886,488)
	pyautogui.typewrite(str(data[mykeys[index]][0])) #Product ID 
	index = index+1
	pyautogui.sleep(1)

	pyautogui.click(750,588)
	#pyautogui.typewrite('Hello')
	pyautogui.scroll(-10)
	pyautogui.sleep(2)

	pyautogui.click(369,429)   
	pyautogui.sleep(2)
	pyautogui.scroll(-60)
	pyautogui.click(382,580)
	pyautogui.sleep(2)


	pyautogui.click(590,852)
	pyautogui.typewrite(str(data[mykeys[index]][0]))  #Display Name
	index = index + 1
	pyautogui.scroll(-10)
	#pyautogHelloHelloui.sleep(2)

	pyautogui.click(599,546)    
	pyautogui.typewrite(str(data[mykeys[index]][0]))  #Description
	index = index + 1
	pyautogui.scroll(-60)

	pyautogui.click(556,642)
	pyautogui.typewrite(str(data[mykeys[index]][0]))  #Note 
	# index = index + 1
	index = 0

	# pyautogui.click(1344,368) #save

if __name__ == "__main__":
	df = pd.read_csv("Upload.csv")
	for i in df.keys():
		if pd.isnull(df[i][0]):
			df[i].fillna("N/A", inplace=True)


	mykeys = df.keys()
	l = len(mykeys)
	# print(mykeys[0])
	# Call the function		
	myFunction(df, mykeys, l)
