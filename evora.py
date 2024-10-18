import sys
import os
import subprocess
import shutil
import requests
from zipfile import ZipFile
from io import BytesIO
import readline
import tempfile


usage_msg = f"""Usage:
evora -w <port>              // to start the web interface
evora -t                    // to start the command line interface
please try '{sys.argv[0]} -h' to see the options"""
help_msg = f"""Usage:
evora -w <port>              // to start the web interface
evora -t                    // to start the command line interface

Options:
    -update     to update the tool
    -h          to get the tool guide
    -activate   to print the environment activation command"""


parentpid = os.getpid()


def update_evora():
    if os.geteuid() != 0:
        print("\033[1;31;40mThis feature must be run as root use sudo to run it. Exiting...\033[0m")
        return

    evora_path = "../Evora"
    if os.path.exists(evora_path):
        shutil.rmtree(evora_path)

    with tempfile.TemporaryDirectory() as temp_path:
        github_url = "https://github.com/The-Ethical-Guy/Evora/archive/main.zip"
        response = requests.get(github_url)

        if response.status_code == 200:
            with ZipFile(BytesIO(response.content), 'r') as zip_file:
                zip_file.extractall(temp_path)

            source_folder = os.path.join(temp_path, "Evora-main")

            if not os.path.exists(evora_path):
                os.makedirs(evora_path)

            for item in os.listdir(source_folder):
                s = os.path.join(source_folder, item)
                d = os.path.join(evora_path, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, False, None)
                else:
                    shutil.copy2(s, d)

            print("\033[1;32;40mEvora updated successfully!\033[0m")
        else:
            print(f"\033[1;31;40mFailed to download Evora from GitHub. Status code: {response.status_code}\033[0m")



def handle_args(user_arg):
    if len(user_arg) < 2 or len(user_arg) > 4:
        print(usage_msg)
        sys.exit(1)

    if user_arg[1] == '-h':
        print(help_msg)
        sys.exit(1)
    
    elif user_arg[1] == '-update':
        update_evora()
        sys.exit(1)
    
    elif user_arg[1] == '-w':
        try:
            port = user_arg[2]
            subprocess.run(["python3.11", "evora-web.py", port])
        except KeyboardInterrupt:
            sys.exit()
        except:
            print(usage_msg)

    elif user_arg[1] == '-t':
        try:
            subprocess.run(["python3.11", "evora-cli.py"])
        except KeyboardInterrupt:
            sys.exit()
            
    elif user_arg[1] == '-activate':
        try:
            with open('evora.info', 'r') as file:
                command = file.read().strip().splitlines()
                print(command[0])
        except KeyboardInterrupt:
            sys.exit()
        except:
            print("please try to setup the tool again using 'sudo bash setup.sh'.")


    else:
        print(usage_msg)

handle_args(sys.argv)
