#!/usr/bin/env python3
"""notewell: a tiny flat-file note taker.

    python3 notewell.py add "some note text"
    python3 notewell.py search query
"""
import sys

NOTES_FILE = "notes.txt"


def add(text):
    with open(NOTES_FILE, "a") as f:
        f.write(text + "\n")


def search(query):
    try:
        with open(NOTES_FILE) as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []
    return [line.rstrip("\n") for line in lines if query in line]


def main():
    if len(sys.argv) < 3:
        sys.exit("usage: notewell.py add|search <text>")
    cmd, arg = sys.argv[1], " ".join(sys.argv[2:])
    if cmd == "add":
        add(arg)
        print(f"added: {arg}")
    elif cmd == "search":
        for line in search(arg):
            print(line)
    else:
        sys.exit(f"unknown command: {cmd}")


if __name__ == "__main__":
    main()
