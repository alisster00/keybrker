import os
import time 
from styles import Styles as st 
from utils import progress_bar, clean_screen
from banner import logo


def load_target_password(password_file="output_password.txt"):
    path = password_file if os.path.isabs(password_file) else os.path.join(os.path.dirname(__file__), password_file)
    if not os.path.exists(path):
        print(f"{st.RED}[ERROR] Create a Dictionary: '{password_file}'")
        input(f"Press ENTER to continue... {st.RESET}")
        return None
   
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            pw = line.strip()
            if pw:
                return pw   

    print(f"{st.RED}[ERROR] '{password_file}' is empty")
    input(f"Press ENTER to continue... {st.RESET}")
    return None

def search_password(password_file="output_password.txt"):
    print(f"{st.BLUE}{logo}")
    target_password = load_target_password(password_file)
    if not target_password:
        return

    print(f"{st.GREEN}[!] Choose the dictionary to search")
    dictionary = input(f"[*] Enter dictionary filename (e.g. 'dict1.txt'):{st.RESET} ").strip()

    if "." not in dictionary:
        dictionary = dictionary + ".txt"

    if not os.path.isfile(dictionary):
        print(f"{st.RED}[ERROR] Dictionari '{dictionary} not found")
        input(f"{st.GREEN}Press ENTER to return... {st.RESET}")
        return 

    with open(dictionary, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    total = len(lines)

    clean_screen()
    print(f"{st.GREEN}{logo}")
    print(f"{st.BLUE}Matching Passwords. Dictionary: '{dictionary}'\n")

    for i, tries in enumerate(lines, 1):
        percent = i / total
        bar = progress_bar(percent)
        status = f"[{i:03}] {bar} {int(percent * 100)}% | Trying: '{tries}'"
        print(status, end="\r", flush=True)
        time.sleep(0.01)

        if tries == target_password:
            clean_screen()
            print(f"{st.BLUE}{logo}")
            print(f"{st.GREEN}Password: '{tries}\nLine: {i:03}\n")
            input(f"Press ENTER to continue... {st.RESET}")
            return

    clean_screen()
    print(f"{st.BLUE}{logo}")
    print(f"{st.RED}[ERROR] Password not found")
    input(f"{st.GREEN}Press ENTER to continue... {st.RESET}")

