import os
from datetime import datetime
import sys
import re
import time
from AIHandler import AIH
from Abil import *
import readline


os.system("cls" if os.name == "nt" else "clear")
logo = """\033[0m
            \033[1;97m\033[1;31;40m░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
\033[0m            \033[1;97m\033[1;31;40m░        ░░  ░░░░  ░░░      ░░░       ░░░░      ░░
\033[0m            \033[1;97m\033[1;31;40m▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒
\033[0m            \033[1;97m\033[1;31;40m▓      ▓▓▓▓▓  ▓▓  ▓▓▓  ▓▓▓▓  ▓▓       ▓▓▓  ▓▓▓▓  ▓
\033[0m            \033[1;97m\033[1;31;40m█  ██████████    ████  ████  ██  ███  ███        █
\033[0m            \033[1;97m\033[1;31;40m█        █████  ██████      ███  ████  ██  ████  █
\033[0m            \033[1;97m\033[1;31;40m██████████████████████████████████████████████████\033[0m  \033[1;93;40mV2.4\033[0m
"""

print(logo)

def print_with_effect(text):
    try:
        for char in text:
            print(char, end='', flush=True)
            time.sleep(0.02) 
    except KeyboardInterrupt:
        print("\033[0;31;40mEvora stopped.\033[0m")
        sys.exit()


print("\033[1;97m\033[1;31;40mEvora:\033[0m ", end='')
print_with_effect("Welcome I'm Evora. Ask me anything, and I'll help. Thanks TheEthicalGuy For Evora.\n\n")

def main():
    print("\033[1;32;40mStarting the session...\033[0m")
    try:
        AIH.StartItUp()
        print("\033[1;32;40mSession Start\033[0m")
    except KeyboardInterrupt:
        print("\033[0;31;40mSession closed.\033[0m")
        sys.exit()
    except:
        print("A STRANGE ERROR OCCURRED, PLEASE RESTART THE TOOL")
        sys.exit()
        
    while True:
        try:
            userInput = input("\033[1;36;40mYou: \033[0m")
            if userInput.startswith("/system"):
                ev_commands = AIH.GetReb(userInput)
                response = sys_execution(ev_commands)
            else:
                response = AIH.GetReb(userInput)
            print(f"\n\033[1;31;40mEvora:\033[0m {response}\n")
        except KeyboardInterrupt:
            print("\033[1;31;40mSession closed.\033[0m")
            sys.exit()

    
    

if __name__ == "__main__":
    main()
