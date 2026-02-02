import os
import time
import random
import itertools
from datetime import datetime
from ui.styles import Styles as st
from ui.banner import logo
from utils.helper import clean_screen
from core.prompts import (
    input_only_letters, 
    input_letters_numbers, 
    input_optional_date, 
    input_multiple_names
)
from utils.paths import (
    dictionaries_dir,
    target_pass_path
)

symbols = ['!', '@', '#', '$', '%', '&', '*', '?']

def user_data_request():
    print(f"{st.BLUE}{logo}")

    first_name = input_only_letters(f"{st.GREEN}[+] First name:{st.RESET} ")
    last_name = input_only_letters(f"{st.GREEN}[+] Last name:{st.RESET} ")
    nickname = input_letters_numbers(f"{st.GREEN}[+] Nickname:{st.RESET} ")
    username = input_letters_numbers(f"{st.GREEN}[+] Username (optional): {st.RESET}")
    
    partner_name = input_only_letters(f"{st.GREEN}[+] Partner name (optional): {st.RESET}")
    pet_names = input_multiple_names(f"{st.GREEN}[+] Pet names (coma separated, optional): {st.RESET}")
    birthday = input_optional_date(f"{st.GREEN}[+] Birthday (DDMMYYYY):{st.RESET} ")
    
    return {
        "personal": {
            "name": first_name,
            "last_name": last_name,
            "nickname": nickname,
        },
        "family": {
            "partner": partner_name,
            "pets": pet_names
        },
        "digital": {
            "username": username
        },
        "dates": {
            "birth": birthday
        }
    }

def select_groups():
    clean_screen()
    print(f"{st.BLUE}{logo}")
    print(f"{st.GREEN}[+] Select data groups to include:{st.RESET}\n")

    def ask(label):
        return input(f"{st.GREEN}[?] Include {label}? (y/n): {st.RESET}").strip().lower() != "n"

    return {
        "personal": ask("personal data"),
        "family": ask("family data"),
        "digital": ask("digital identity"),
        "dates": ask("dates")
    }

def process_date(date_str):
    try:
        this_date = datetime.strptime(date_str, "%d%m%Y")
        return {
            "day": this_date.strftime("%d"),
            "month_num": this_date.strftime("%m"),
            "month_name": this_date.strftime("%B").lower(),
            "year": this_date.strftime("%Y"),
            "year_short": this_date.strftime("%y")
        }

    except (ValueError, TypeError):
        print(f"\n{st.YELLOW}[WARNING] Invalid date entered.{st.RESET}\n")
        return None
    
def build_parts(user_data, enabled_groups):
    parts = []

    if enabled_groups.get("personal"):
        personal = user_data.get("personal", {})
        for key in ("name", "last_name", "nickname"):
            value = personal.get(key)
            if value:
                parts.append(value)

    if enabled_groups.get("family"):
        family = user_data.get("family", {})
        if family.get("partner"):
            parts.append(family["partner"])
        for pet in family.get("pets", []):
            parts.append(pet)

    if enabled_groups.get("digital"):
        username = user_data.get("digital", {}).get("username")
        if username:
            parts.append(username)  

    if enabled_groups.get("dates"):
        birth = user_data.get("dates", {}).get("birth")
        date_info = process_date(birth)
        if date_info:
            parts.extend(date_info.values())

    seen = set()
    clean = []
    for p in parts:
        if p not in seen:
            seen.add(p)
            clean.append(p)

    return clean

def estimate_pass_count(parts):
    n = len(parts)
    if n < 2:
        return 0 

    perm_2 = n * (n - 1)
    perm_3 = n * (n - 1) * (n - 2) if n >= 3 else 0 

    avg_variants = 13
    return (perm_2 + perm_3) * avg_variants

def generate_passwords(user_data, enabled_groups):
    parts = build_parts(user_data, enabled_groups)
    if len(parts) < 2:
        return []

    variants = set()
    generated_count = 0
    start_time = time.time()
    enable_sleep = True

    clean_screen()
    print(f"{st.BLUE}{logo}")
    print(f"{st.GREEN}Generating Passwords. It may take a few minutes\n")

    for i in range(2, 4):
        for combo in itertools.permutations(parts, i):
            base = ''.join(combo)

            candidates = [
                base, 
                base.lower(), 
                base.capitalize(), 
                base.upper()
            ]

            for _ in range(3):
                symbol = random.choice(symbols)
                number = str(random.randint(10, 99))

                candidates.extend([
                    base + symbol + number,
                    symbol + base + number,
                    number + base + symbol
                ])

            for pwd in candidates:
                if pwd not in variants:
                    variants.add(pwd)
                    generated_count += 1
                    print(f"[{generated_count}] '{pwd}'", end="\r", flush=True)

                    if enable_sleep:
                        time.sleep(0.01)
                        if generated_count > 5000:
                            enable_sleep = False

    elapsed = time.time() - start_time
    clean_screen()
    print(f"{st.BLUE}{logo}")
    print(f"{st.GREEN}Total passwords generated: {generated_count}{st.RESET}")
    print(f"{st.GREEN}Elapsed time: {elapsed:.2f} seconds{st.RESET}\n")

    return list(variants)

def save_passwords(passwords, output_file="dictionary.txt"):
    with open(output_file, "w", encoding="utf-8") as f:
        for pwd in passwords:
            f.write(pwd + "\n")
    print(f"{st.GREEN}Dictionary saved as '{output_file}'")

def target_pass(passwords, output_file="output_password.txt"):
    if not passwords:
        return

    target = random.choice(passwords)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"{target}\n")
    input(f"Press ENTER to continue... {st.RESET}")

def dictionary_generator():
    user_data = user_data_request()
    enabled_groups = select_groups()

    parts = build_parts(user_data, enabled_groups)
    
    if len(parts) < 2:
        clean_screen()
        print(f"{st.BLUE}{logo}")
        print(f"{st.RED}[ERROR] Not enough user_data to generate passwords. {st.RESET}\n")
        input(f"{st.GREEN}Press ENTER to continue... {st.RESET}")
        return

    estimated = estimate_pass_count(parts)

    clean_screen()
    print(f"{st.BLUE}{logo}")
    print(f"{st.YELLOW}Estimated passwords to generate: ~{estimated}{st.RESET}")
    
    confirm = input(f"{st.GREEN}[!] Continue? (y/n): {st.RESET}").lower().strip()
    if confirm != "y":
        return

    output_name = input(f"{st.GREEN}[*] Output file name (default: 'dictionary.txt'):{st.RESET} ").strip()
    if not output_name:
        output_name = "dictionary.txt"
    elif "." not in output_name:
        output_name += ".txt"

    dictionaries_dir.mkdir(parents=True, exist_ok=True)
    dictionary_path = dictionaries_dir / output_name

    passwords = generate_passwords(user_data, enabled_groups)

    if not passwords:
        return

    save_passwords(passwords, output_file=dictionary_path)
    target_pass(passwords, output_file=target_pass_path)
