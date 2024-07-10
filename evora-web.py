from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os
from AIHandler import AIH
from Abil import *
import sys
import readline
import time
import re
import subprocess


#colors & fonts
normal_font = '\033[0m'
bond = '\033[1;97m'
red = '\033[1;31;40m'
skyblue = '\033[1;92;40m'
blue = '\033[1;36;40m'
orange = '\033[0;32;40m'
yellow = '\033[1;93;40m'
green = '\033[1;32;40m'



os.system("cls" if os.name == "nt" else "clear")
logo = """\033[0m
            \033[1;97m\033[1;31;40m░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
\033[0m            \033[1;97m\033[1;31;40m░        ░░  ░░░░  ░░░      ░░░       ░░░░      ░░
\033[0m            \033[1;97m\033[1;31;40m▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒
\033[0m            \033[1;97m\033[1;31;40m▓      ▓▓▓▓▓  ▓▓  ▓▓▓  ▓▓▓▓  ▓▓       ▓▓▓  ▓▓▓▓  ▓
\033[0m            \033[1;97m\033[1;31;40m█  ██████████    ████  ████  ██  ███  ███        █
\033[0m            \033[1;97m\033[1;31;40m█        █████  ██████      ███  ████  ██  ████  █
\033[0m            \033[1;97m\033[1;31;40m██████████████████████████████████████████████████\033[0m  \033[1;93;40mV2.6\033[0m
"""

print(logo)

def print_with_effect(text):
    try:
        for char in text:
            print(char, end='', flush=True)
            time.sleep(0.02) 
    except KeyboardInterrupt:
        print("\033[1;31;40mEvora stopped.\033[0m")
        sys.exit()


print("\033[1;97m\033[1;31;40mEvora:\033[0m ", end='')
print_with_effect("Welcome I'm Evora. Ask me anything, and I'll help. Thanks TheEthicalGuy For Evora.\n\n")


print("\033[1;32;40mStarting the server...")
try:
    AIH.StartItUp()
except KeyboardInterrupt:
    print("\033[1;31;40mEvora stopped.\033[0m")
    sys.exit()
except:
    print("A STRANGE ERROR OCCURRED, PLEASE RESTART THE TOOL")
    sys.exit()

try:
    usrportnum = int(sys.argv[1])
    if usrportnum <65536:
        port = usrportnum
    else:
        print("\033[0;31;40mplease enter a valid port number\033[0m")
        sys.exit()
except IndexError:
    port = 8080

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("templates/index.html", "rb") as file:
                self.wfile.write(file.read())
        elif parsed_path.path == "/main.css":
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.end_headers()
            with open("templates/style/main.css", "rb") as file:
                self.wfile.write(file.read())
        elif parsed_path.path == "/send.js":
            self.send_response(200)
            self.send_header("Content-type", "application/javascript")
            self.end_headers()
            with open("templates/js/send.js", "rb") as file:
                self.wfile.write(file.read())
        elif parsed_path.path == "/textbox.js":
            self.send_response(200)
            self.send_header("Content-type", "application/javascript")
            self.end_headers()
            with open("templates/js/textbox.js", "rb") as file:
                self.wfile.write(file.read())
        elif parsed_path.path == "/fonts/BlackCaps.otf":
            self.send_response(200)
            self.send_header("Content-type", "font/otf")
            self.end_headers()
            with open("templates/style/fonts/BlackCaps.otf", "rb") as file:
                self.wfile.write(file.read())
        elif parsed_path.path == "/fonts/OCRAStd.otf":
            self.send_response(200)
            self.send_header("Content-type", "font/otf")
            self.end_headers()
            with open("templates/style/fonts/OCRAStd.otf", "rb") as file:
                self.wfile.write(file.read())
        elif parsed_path.path == "/style/img/copy.png":
            self.send_response(200)
            self.send_header("Content-type", "image/png")
            self.end_headers()
            with open("templates/style/img/copy.png", "rb") as file:
                self.wfile.write(file.read())
        elif parsed_path.path == "/evanai.ico":
            self.send_response(200)
            self.send_header("Content-type", "image/ico")
            self.end_headers()
            with open("templates/style/img/evanai.ico", "rb") as file:
                self.wfile.write(file.read())

        elif parsed_path.path == "/get_response":
            query_params = parse_qs(parsed_path.query)
            if "message" in query_params:
                message = query_params["message"][0]
                response = AIH.GetReb(message)  #
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(response.encode())
            else:
                self.send_error(400, "Bad Request")
            
           
          
        elif parsed_path.path == "/exec_system":
            query_params = parse_qs(parsed_path.query)
            if "command" in query_params:
                message = query_params["command"][0]
                ev_commands = AIH.GetReb(message)
                response = sys_execution(ev_commands)
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(response.encode())
            else:
                self.send_error(400, "Bad Request")
                
                
        else:
            self.send_error(404, "Not Found")



def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=port):
    server_address = ("0.0.0.0", port)
    httpd = server_class(server_address, handler_class)
    print(f"\033[1;97mThe server is running on: \033[0;36;40mhttp://127.0.0.1:{server_address[1]}\n\n\n")
    print("\033[1;97m_________________THE-TRAFFIC_________________\033[0m")
    
    try:
        httpd.serve_forever()
    except OSError:
        print("\033[0;31;40mThis port already in used.\033[0m")
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("\033[1;31;40mServer stopped.\033[0m")

if __name__ == "__main__":
    run()
