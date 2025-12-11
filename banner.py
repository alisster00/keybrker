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

project_info = f"[+] Project Name: KeyBreaker (Sim Mode)\n[+] Version:"

autor_info = r"""
[+] Autor: Alister
[+] GitHub: https://github.com/alisster00
[+] Email: akaristr@protonmail.com
"""
def check_version():
    with open("version.json", "r", encoding="utf-8") as file:
        version = json.load(file)
        return f"{version['version']}"

def get_info():
    print(f"{st.GREEN}{logo}")
    print(project_info, check_version(), autor_info)
    input("Press ENTER to return... ")

def show_banner():
    print(f"{st.BLUE}{logo}")
    print(f"Version: {check_version()}")
    print(f"{st.GREEN}{menu}")

