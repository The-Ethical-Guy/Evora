#!/bin/bash

clear
echo -e "            \033[1;97m\033[1;31;40m░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░"
echo -e "\033[0m            \033[1;97m\033[1;31;40m░        ░░  ░░░░  ░░░      ░░░       ░░░░      ░░"
echo -e "\033[0m            \033[1;97m\033[1;31;40m▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒"
echo -e "\033[0m            \033[1;97m\033[1;31;40m▓      ▓▓▓▓▓  ▓▓  ▓▓▓  ▓▓▓▓  ▓▓       ▓▓▓  ▓▓▓▓  ▓"
echo -e "\033[0m            \033[1;97m\033[1;31;40m█  ██████████    ████  ████  ██  ███  ███        █"
echo -e "\033[0m            \033[1;97m\033[1;31;40m█        █████  ██████      ███  ████  ██  ████  █"
echo -e "\033[0m            \033[1;97m\033[1;31;40m██████████████████████████████████████████████████\033[0m  \033[1;93;40mInstaller\033[0m"
echo -e ""
echo -e "\033[1;33m FOR DONATIONS"
echo -e "\033[1;32m BTC: bc1qeqn0lcykrpcvkgcyse4vphrqmffu26sz9dnuru"
echo -e "\033[1;32m LTC: ltc1q4u7prf66nk9d5u3s0ha30ffcfws7vhq7dad946"

tool_name="evora"
script_path="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"  

venv_path="$script_path/venvEvora"


if [ -f "$script_path/requirements.txt" ]; then
    echo ""
    echo -e "\033[1;32m Creating virtual environment..."

    apt install python3.12-venv
    
    python3 -m venv "$venv_path"


    source "$venv_path/bin/activate"

    echo -e "\033[1;32m Installing requirements..."


    pip install -r "$script_path/requirements.txt" > pip_install_output.txt 2>&1
    rm pip_install_output.txt
    sleep 5

    if [ $? -eq 0 ]; then
        echo " done :)"
        echo -e "\033[1;97m type 'source $venv_path/bin/activate' to activate the virtual environment"
        echo -e "\033[1;97m and then 'evora -h' to know how to use it"
    else
        echo -e "\033[1;31;40m there is an error occurred during installation"
    fi
else
    echo -e "\033[1;31;40m you need to reinstall the tool"
    echo -e "\033[1;32m Creating virtual environment..."


    python3 -m venv "$venv_path"


    source "$venv_path/bin/activate"

    echo -e "\033[1;32m Installing required packages..."


    pip install readline google google-generativeai > pip_install_output.txt 2>&1
    rm pip_install_output.txt
    sleep 5

    if [ $? -eq 0 ]; then
        echo " done :)"
        echo -e "\033[1;97m type 'source $venv_path/bin/activate' to activate the virtual environment"
        echo -e "\033[1;97m and then 'evora -h' to know how to use it"
    else
        echo -e "\033[1;31;40m there is an error occurred during installation"
    fi
fi
