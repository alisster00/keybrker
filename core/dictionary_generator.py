import time
import random
import itertools
from datetime import datetime
from ui.styles import Styles as st
from ui.banner import logo
from utils.helper import clean_screen
from core.prompts import input_only_letters, input_letters_numbers, input_optional_date, input_multiple_names

symbols = ['!', '@', '#', '$', '%', '&', '*', '?']

def user_data_request():
    print(f"{st.BLUE}{logo}")

    first_name = input_only_letters(f"{st.GREEN}[+] First name:{st.RESET} ")
    last_name = input_only_letters(f"{st.GREEN}[+] Last name:{st.RESET} ")
    nickname = input_letters_numbers(f"{st.GREEN}[+] Nickname:{st.RESET} ")
    username = input_letters_numbers(f"{st.GREEN}[+] Username (optional): {st.RESET}")
    
    partner_name = input_only_letters(f"{st.GREEN}[+] Parner name (optional): {st.RESET}")

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

def build_parts(user_data):
    parts = []

    personal = user_data.get("personal", {})
    for key in ("first_name", "last_name", "nickname"):
        value = personal.get(key)
        if value:
            parts.append(value)

    family = user_data.get("family", {})
    partner = family.get("partner")
    if partner:
        parts.append(partner)
    pets = family.get("pets", [])
    for pet in pets:
        parts.append(pet)

    digital = user_data.get("digital", {})
    username = digital.get("username")
    if username:
        parts.append(username)  

    dates = user_data.get("dates", {})
    birthday = dates.get("birth")

    if birthday:
        date_info = process_date(birthday)
        if date_info:
            parts.extend([
                date_info["day"],
                date_info["month_num"],
                date_info["month_name"],
                date_info["year"],
                date_info["year_short"]
            ])

    seen = set()
    clean_parts = []
    for p in parts:
        if p not in seen:
            seen.add(p)
            clean_parts.append(p)

    return clean_parts

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

    except ValueError:
        print(f"\n{st.YELLOW}[WARNING] Invalid date entered.{st.RESET}\n")
        return None

def generate_passwords(user_data):
    parts = build_parts(user_data)

    if len(parts) < 2:
        clean_screen()
        print(f"{st.BLUE}{logo}")
        print(f"{st.RED}[ERROR] Not enough user_data to generate passwords. {st.RESET}\n")
        input(f"{st.GREEN}Press ENTER to continue... {st.RESET}")
        return []

    variants = set()
    start_time = time.time()
    generated_count = 0
    enable_sleep = True

    for i in range(2, 4):
        for combo in itertools.permutations(parts, i):
            base = ''.join(combo)
            candidates = [
                base, 
                base.lower(), 
                base.capitalize(), 
                base.upper()
            ]
            #build_parts(user_data)

            for _ in range(3):
                symbol = random.choice(symbols)
                number = str(random.randint(10, 99))

                candidates.extend([
                    base + symbol + number,
                    symbol + base + number,
                    number + base + symbol
                ])

            clean_screen()
            print(f"{st.BLUE}{logo}")
            print(f"{st.GREEN}Generating Passwords. It may take a few minutes\n")

            for pwd in candidates:
                prev_len = len(variants)
                variants.add(pwd)

                if len(variants) > prev_len:
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
        for c in passwords:
            f.write(c + "\n")
    print(f"{st.GREEN}Dictionary saved as '{output_file}'")

def target_pass(passwords, output_file="output_password.txt"):
    if not passwords:
        return

    target = random.choice(passwords)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"{target}\n")
    input(f"Press ENTER to continue... {st.RESET}")

def dictionary_generator():
    user_info = user_data_request()

    output_name = input(f"{st.GREEN}[*] Output file name (default: 'dictionary.txt'):{st.RESET} ").strip()
    if not output_name:
        output_name = "dictionary.txt"

    elif "." not in output_name:
        output_name = output_name + ".txt"

    gen_passwords = generate_passwords(user_info)

    if not gen_passwords:
        return

    save_passwords(gen_passwords, output_file=output_name)
    target_pass(gen_passwords, output_file="output_password.txt")
