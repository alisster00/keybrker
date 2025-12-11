import time
import random
import itertools
from datetime import datetime
from styles import Styles as st
from banner import logo
from utils import clean_screen

symbols = ['!', '@', '#', '$', '%', '&', '*', '?']

def user_data_request():
    print(f"{st.BLUE}{logo}")
    name = input(f"{st.GREEN}[+] First name:{st.RESET} ").strip()
    last_name = input(f"{st.GREEN}[+] Last name:{st.RESET} ").strip()
    nickname = input(f"{st.GREEN}[+] Nickname:{st.RESET} ").strip()
    birthday = input(f"{st.GREEN}[+] Birthday (DDMMYYYY):{st.RESET} ").strip()

    return {
        "name": name,
        "last_name": last_name,
        "nickname": nickname,
        "birthday": birthday
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

    except ValueError:
        print(f"\n{st.YELLOW}[WARNING] Invalid date entered.{st.RESET}\n")
        return None

def generate_passwords(data):
    date_info = process_date(data.get("birthday", "").strip())
    
    parts = [
        data.get("name", "").strip(),
        data.get("last_name", "").strip(),
        data.get("nickname", "").strip(),
    ]

    parts = [p for p in parts if p]

    if date_info:
        parts.extend([
            date_info["day"],
            date_info["month_num"],
            date_info["month_name"],
            date_info["year"],
            date_info["year_short"]
        ])

    if len(parts) < 2:
        clean_screen()
        print(f"{st.BLUE}{logo}")
        print(f"{st.RED}[ERROR] Not enough data to generate passwords. {st.RESET}\n")
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

    gen_passwords = generate_passwords(user_info)

    if not gen_passwords:
        return

    save_passwords(gen_passwords, output_file=output_name)
    target_pass(gen_passwords, output_file="output_password.txt")
