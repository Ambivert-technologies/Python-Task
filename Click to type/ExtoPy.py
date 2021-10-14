import pandas as pd
import pyautogui
from pynput.mouse import Controller, Listener
import time

class MyClass:
    
    def __init__(self):
        self.counter = 0        
        
        
    def write_data(self, x, y, data):
        pyautogui.moveTo(x, y)
        pyautogui.click(x, y)
        pyautogui.write(data, interval=0)
        
    def click_event(self, x, y, button, pressed):
        global previous_left, all_data
        
        double_click_left = False
        
        mouse = Controller()
        x, y = mouse.position  
        
        if pressed:
            current_left = time.time()
            diff_left = current_left - previous_left
            
            if diff_left < 0.3:
                
                # WRITE THE EXCEL data
                self.write_data(x, y, all_data[self.counter])
                self.counter += 1
                
                double_click_left = True
                
            previous_left = current_left
        
        if double_click_left:
            # Stop listener
            return True        
            
            
if __name__ == "__main__":
    
    df = pd.read_excel("data.xlsx")
    keys = df.keys()
    all_data = []
    for i in range(len(keys)):
        for j in keys:
            all_data.append(df[j][i])    
    
    obj = MyClass()
    #obj.read_data()
    previous_left = 0
    
    with Listener(on_click=obj.click_event) as listener:
        listener.join()