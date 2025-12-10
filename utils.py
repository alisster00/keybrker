import os

def clean_screen():
    os.system("clear" if os.name == "posix" else "cls")

def progress_bar(percent, width=20):
    progress = int(percent * width)
    
    a = "#"
    b = "-"
    return f"[{a * progress}{b * (width - progress)}]"


