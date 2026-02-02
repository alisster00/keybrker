from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

data_dir = project_root / "data"

dictionaries_dir = data_dir / "dictionaries"

default_dict_path = dictionaries_dir / "dictionary.txt"
target_pass_path = data_dir / "output_password.txt"
