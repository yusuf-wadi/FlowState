import numpy as np
import utils
from time import sleep
from selenium import common
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from eeg import Band, BUFFER_LENGTH, EPOCH_LENGTH, SHIFT_LENGTH, INDEX_CHANNELS, get_inlet, init_buffers, brain_read
# take in lsl stream, compute alpha power, and speed up or slow down video accordingly



# setup selenium

def setup():
    # define the path to the chromedriver executable
    driver_path = "C:/Program Files/BraveSoftware/Brave-Browser-Nightly/Application/brave.exe"

    b_path = driver_path
    
    # define the path to the user profile
    userpp = r"C:\Users\thewa\AppData\Local\BraveSoftware\Brave-Browser-Nightly\User Data"
    options = webdriver.ChromeOptions()
    options.binary_location = b_path

    # set dl options
    #prefs = {"download.default_directory": "C:/Users/thewa/Desktop/"}
    # e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
    
    userD = f"--user-data-dir={userpp}"
    options.add_argument(userD)
    options.add_argument(r'--profile-directory=Default')  # e.g. Profile 3
    #options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    
    return browser

# def brain_read(inlet):

if __name__ == "__main__":

    inlet = get_inlet()

    buffers = init_buffers(inlet)

    """ 3. GET DATA """

    # The try/except structure allows to quit the while loop by aborting the
    # script with <Ctrl-C>
    print('Press Ctrl-C in the console to break the while loop.')

    # open browser to youtube, wait for user to select video, then begin processing alpha band power

    try:
        
        # open browser to youtube
        driver = setup()
        driver.get("https://www.youtube.com/")
        
        band = Band
        alpha = band.Alpha
        
        while True:
            #begin computing alpha power
            
            buffers = brain_read(inlet, buffers, print_output=True)
            
            # once video is found, begin controlling playback speed based on alpha power
            
            if buffers[1][1][-1, alpha] < 0.9:
                print("sped up")
                driver.execute_script('''document.getElementsByClassName("video-stream html5-main-video")[0].playbackRate = 2.0''')
            else:
                print('slowed down')
                driver.execute_script('''document.getElementsByClassName("video-stream html5-main-video")[0].playbackRate = 0.5''')
    except KeyboardInterrupt:
        print('Closing!')
        
        
         
