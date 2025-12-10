from utils import clean_screen
from banner import show_banner, get_info
from styles import Styles as st 
from dictionary_generator import dictionary_generator
from attack_simulator import search_password

def main_menu():
    while True:
        clean_screen()
        show_banner()

        choice = input(f"What do you wanna do? {st.RESET}").strip()

        if choice == "1":
            dictionary_generator()

        elif choice == "2":
            output_file = input("File name: ")
            search_password(output_file)

        elif choice == "3":
            clean_screen
            get_info()

        elif choice == "4":
            print(f"See you later!")
            break

        else:
            input(f"{st.RED}[ERROR] Press ENTER and try again... ")

main_menu()
