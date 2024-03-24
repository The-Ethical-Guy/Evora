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
{sys.argv[0]} -w <port>              // to start the web interface
{sys.argv[0]} -t                    // to start the command line interface
please try '{sys.argv[0]} -h' to see the options"""
help_msg = f"""Usage:
{sys.argv[0]} -w <port>              // to start the web interface
{sys.argv[0]} -t                    // to start the command line interface

Options:
    -update     to update the tool
    -h          to get the tool guide"""


parentpid = os.getpid()


def update_evora():
    evora_path = "../Evora"
    if os.path.exists(evora_path):
        shutil.rmtree(evora_path)

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_path:
        github_url = "https://github.com/The-Ethical-Guy/Evora/archive/main.zip"
        response = requests.get(github_url)

        if response.status_code == 200:
            with ZipFile(BytesIO(response.content), 'r') as zip_file:
                zip_file.extractall(temp_path)


            source_folder = os.path.join(temp_path, "Evora-main")
            shutil.move(source_folder, evora_path)

            print("Evora updated successfully!")
        else:
            print(f"Failed to download Evora from GitHub. Status code: {response.status_code}")


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
            subprocess.run(["python3", "evora-web.py", port])
        except KeyboardInterrupt:
            sys.exit()
        except:
            print(usage_msg)

    elif user_arg[1] == '-t':
        try:
            subprocess.run(["python3", "evora-cli.py"])
        except KeyboardInterrupt:
            sys.exit()
    
    else:
        print(usage_msg)

handle_args(sys.argv)
