from utils.helper import clean_screen
from ui.banner import show_banner, get_info, logo
from ui.styles import Styles as st 
from core.dictionary_generator import dictionary_generator
from core.attack_simulator import search_password, load_target_password

def main_menu():
    while True:
        clean_screen()
        show_banner()

        choice = input(f"What do you want to do? {st.RESET}").strip().lower()

        if choice in ["q", "quit", "exit"]:
            print(f"\n{st.GREEN}See you later!{st.RESET}")
            break

        if choice == "1":
            clean_screen()
            dictionary_generator()

        elif choice == "2":
            clean_screen()
            search_password()

        elif choice == "3":
            clean_screen()
            get_info()

        elif choice == "4":
            print(f"\n{st.GREEN}See you later!{st.RESET}")
            break

        else:
            print(f"{st.RED}[ERROR] Invalid option.")
            input(f"{st.GREEN}Press ENTER to try again... {st.RESET}")

if __name__ == "__main__":
    main_menu()
