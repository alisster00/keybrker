import os
import time 
from styles import Styles as st 
from utils import progress_bar, clean_screen


def load_target_password(password_file="output_password.txt"):
    path = password_file if os.path.isabs(password_file) else os.path.join(os.path.dirname(__file__), password_file)
    if not os.path.exists(path):
        print(f"{st.RED}[ERROR] Create a Dictionary: '{password_file}'{st.RESET}")
        return None
   
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            pw = line.strip()
            if pw:
                return pw   

    print(f"{st.RED}[ERROR] '{password_file}' is empty{st.RESET}")
    return None

def search_password(output_file, password_file="output_password.txt"):
    target_password = load_target_password(password_file)
    if not target_password:
        return

    with open(output_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    total = len(lines)

    for i, tries in enumerate(lines, 1):
        percent = i / total
        bar = progress_bar(percent)
        status = f"{i:03} Matching Password {bar} {int(percent * 100)}% | Trying: '{tries}'"
        print(status, end="\r", flush=True)
        time.sleep(0.05)

        if tries == target_password:
            clean_screen()
            print(f"Password: '{tries}\nLine: {i:03}\n")
            input(f"Press ENTER to continue... {st.RESET}")

            return

    print(f"{st.RED}[ERROR] Password not found{st.RESET}")

