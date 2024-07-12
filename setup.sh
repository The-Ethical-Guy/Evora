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
echo -e "\033[1;32m BTC: bc1qhpez52mku3d532xsrz7f0zn5l85e2q47zsr6l2"
echo -e "\033[1;32m LTC: ltc1qls08k4s7gzuu2dx83znpng20vw86uc2h8xnwsc"

# Check if the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo -e "\033[1;97m\033[1;31;40mThis script must be run as root use sudo to run it. Exiting...\033[0m"
    exit 1
fi

tool_name="evora"
script_path="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"  

echo -e "#!/bin/bash\ncd \"$script_path\"\npython3 \"$script_path/$tool_name.py\" \"\$@\"" > $tool_name
chmod +x $tool_name
sudo mv $tool_name /usr/local/bin/

venv_path="$script_path/venvEvora"

# Install python3-venv if not already installed
if ! dpkg -s python3-venv &> /dev/null; then
    echo -e "\033[1;33mInstalling python3-venv package...\033[0m"
    sudo apt install python3-venv -y > installation_output.txt 2>&1
    sudo apt install python3-pip -y > installation_output.txt 2>&1
    sudo apt install python3-virtualenv -y > installation_output.txt 2>&1
    if [ $? -ne 0 ]; then
        echo -e "\033[1;31mFailed to install python3-venv. Check installation_output.txt for details.\033[0m"
        exit 1
    fi
fi


if [ -f "$script_path/requirements.txt" ]; then
    echo ""
    echo -e "\033[1;32m Creating virtual environment..."

    
    python3 -m venv "$venv_path" > installation_output.txt 2>&1


    source "$venv_path/bin/activate"

    echo -e "\033[1;32m Installing requirements..."

    sudo apt-get install libreadline-dev -y > installation_output.txt 2>&1
    pip install pyproject-toml > installation_output.txt 2>&1
    pip install -r "$script_path/requirements.txt" > installation_output.txt 2>&1
    sleep 5

    if [ $? -eq 0 ]; then
        echo -e "source '$venv_path/bin/activate'" > evora.info
        echo " done :)"
        echo -e "\033[1;97m type (source '$venv_path/bin/activate') to activate the virtual environment"
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


    sudo apt-get install libreadline-dev -y > installation_output.txt 2>&1
    pip install pyproject-toml > installation_output.txt 2>&1
    pip install readline google google-generativeai requests > installation_output.txt 2>&1
    sleep 5

    if [ $? -eq 0 ]; then
        echo -e "source '$venv_path/bin/activate'" > evora.info
        echo " done :)"
        echo -e "\033[1;97m type (source '$venv_path/bin/activate') to activate the virtual environment"
        echo -e "\033[1;97m and then 'evora -h' to know how to use it"
    else
        echo -e "\033[1;31;40m there is an error occurred during installation"
    fi
fi
