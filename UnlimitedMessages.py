"""
import pywhatkit as pw
pw.sendwhatmsg('Give a phone number with country code', 'Message you want to send ', hour, minute) 
This will send "Emon is the king" message to that whatsapp number
Only one time message will be sent.
"""

import pyautogui as py
import time

while True:
    # After how much time message will repeatedly be sent
    time.sleep(2 ) # After 3 three seconds message will be repeated
    py.typewrite("Emon")
    py.press('enter')

"""
    After running the program we just put the cursor in the text box where we want to send messages.
    This loop will go on until we stop this manually.
"""
