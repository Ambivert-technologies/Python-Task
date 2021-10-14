from selenium import webdriver
import os
import time
def processed_file():
    all_packages = []
    with open("packages.txt", "r") as f:
        for i in f.readlines():
            all_packages.append(i)
    print("All packages==>",all_packages)
    clean_packeages = []
    for i in all_packages:
        index = i.index(":")
        clean_packeages.append(i[:index])      
    print("Clean packages==>",clean_packeages)
    
    return clean_packeages
    
def navigate_website(driver):
    counter = 0
    for i in packages:
        url = f"https://pub.dev/packages/{i}/license"
        driver.get(url)
        time.sleep(3)
        mytext = get_text(driver)
        mytext = ":::::::::::::::::::::::::::::::::::::::::"+str(i)+":::::::::::::::::::::::::::::::::::::::::::::::::::::::\n"+str(mytext)+"\n\n\n\n"
        write_text(mytext)


def get_text(driver):
    t = driver.find_element_by_tag_name("pre")
    return t.text

def write_text(text):
    f = open("license.txt", "a")
    f.write(text)
    f.close()

if __name__=="__main__":
    packages = processed_file()
    driver = webdriver.Chrome(executable_path="./chromedriver")
    navigate_website(driver)
    
    print("-------------DONE---------------")