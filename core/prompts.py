from ui.styles import Styles as st

def input_only_letters(prompt):
    while True:
        value = input(prompt).strip()

        if not value:
            return ""

        if value.isalpha():
            return value.lower()

        print(f"{st.RED}[ERROR] Only letters are allowed. Please try again")
        input(f"{st.GREEN}Press ENTER to continue... {st.RESET}")

def input_letters_numbers(prompt):
    while True:
        value = input(prompt).strip()
        if not value:
            return ""
        if value.isalnum():
            return value.lower()

        print(f"{st.RED}[ERROR] Only letters and numbers are allowed. Please try again")
        input(f"{st.GREEN}Press ENTER to continue... {st.RESET}")

def input_optional_date(prompt):
    value = input(prompt).strip()
    return value

def input_multiple_names(prompt):
    value = input(prompt).strip()
    if not value:
        return []

    names = [v.strip().lower() for v in value.split(",") if v.strip()]
    return [n for n in names if n.replace(" ", "").isalpha()]

