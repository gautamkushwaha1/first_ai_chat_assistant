import os

START_SEQUENCE = "\033[91m" # ansi code for red text
END_SEQUENCE = "\033[0m" #ansi code for white text


def log(text):
  if os.getenv("DEBUG") == "True":
    print(f"{START_SEQUENCE} {text} {END_SEQUENCE}")
