import json
from styles import Styles as st 

logo = r"""
 _  __          ____       _             
| |/ /___ _   _| __ ) _ __| | _____ _ __ 
| ' // _ \ | | |  _ \| '__| |/ / _ \ '__|
| . \  __/ |_| | |_) | |  |   <  __/ |   
|_|\_\___|\__, |____/|_|  |_|\_\___|_|   
          |___/                          
"""
menu = r"""
[!] KeyBreaker (Sim Mode)

[1] Generate a Dictionary
[2] Brute Force Attack (Sim)
[3] Get Project Info
[4] Exit

"""

info = r"""
[+] Project Name: KeyBreaker (Simulation Mode)
[+] Autor: Alister
[+] GitHub: https://github.com/alisster00
[+] Email: akaristr@protonmail.com

"""

def check_version():
    with open("version.json", "r", encoding="utf-8") as file:
        version = json.load(file)
        return f"{version['version']}"

def get_info():
    print(info)
    input("Press ENTER to go back")

def show_banner():
    print(f"{st.BLUE}{logo}")
    print(f"Version: {check_version()}")
    print(f"{st.GREEN}{menu}")

