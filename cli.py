#!/usr/bin/env python3
"""
AI Agent — CLI interface
Run: python cli.py
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

import agent
import history as hist

# Initialize DB
hist.init_db()

# File type menu
FILE_TYPES = {
    "1": ("notes",  "Study Notes (.txt)"),
    "2": ("word",   "Word Document (.docx)"),
    "3": ("pdf",    "PDF Report (.pdf)"),
    "4": ("excel",  "Spreadsheet (.xlsx)"),
    "5": ("ppt",    "Presentation (.pptx)"),
}

# Colors (for better CLI UI)
RESET  = "\033[0m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
RED    = "\033[91m"
DIM    = "\033[2m"
BOLD   = "\033[1m"


# ─── HEADER ─────────────────────────────

def header():
    print(f"\n{CYAN}{'─'*50}")
    print(f"  {BOLD}AI Agent{RESET}{CYAN}  //  CLI")
    print(f"{'─'*50}{RESET}")

    if not os.getenv("OPENROUTER_API_KEY"):
        print(f"{RED}⚠️ Warning: OPENROUTER_API_KEY not set{RESET}")


# ─── GENERATE FILE ─────────────────────

def menu_generate():
    print(f"\n{DIM}File types:{RESET}")
    for k, (_, label) in FILE_TYPES.items():
        print(f"  {CYAN}{k}{RESET}. {label}")

    choice = input(f"\n{DIM}Type (1-5):{RESET} ").strip()
    if choice not in FILE_TYPES:
        print(f"{RED}Invalid choice{RESET}")
        return

    file_type, label = FILE_TYPES[choice]
    topic = input(f"{DIM}Topic:{RESET} ").strip()

    if not topic:
        print(f"{RED}Topic cannot be empty{RESET}")
        return

    print(f"\n{DIM}Generating {label}...{RESET}", end="", flush=True)

    try:
        filepath, filename = agent.generate_file(file_type, topic)
        hist.log_generation(file_type, topic, filename)

        print(f"\r{GREEN}✓ {filename}{RESET}")
        print(f"{DIM}Saved to: {filepath}{RESET}")

    except Exception as e:
        print(f"\r{RED}✗ Error: {e}{RESET}")


# ─── CHAT ─────────────────────────────

def menu_chat():
    print(f"\n{DIM}Chat mode — type 'exit' to go back{RESET}\n")

    while True:
        try:
            msg = input(f"{CYAN}You:{RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not msg:
            continue
        if msg.lower() == "exit":
            break

        print(f"{YELLOW}AI:{RESET} ", end="", flush=True)

        try:
            for chunk in agent.chat_stream(msg):
                print(chunk, end="", flush=True)
            print()
        except Exception as e:
            print(f"{RED}Error: {e}{RESET}")


# ─── HISTORY ───────────────────────────

def menu_history():
    items = hist.get_history(limit=10)

    if not items:
        print(f"\n{DIM}No history yet{RESET}")
        return

    print(f"\n{DIM}Recent generations:{RESET}")
    print(f"{'TYPE':<10} {'TOPIC':<25} {'FILE':<25} {'TIME'}")
    print("-" * 70)

    for item in items:
        time = item["created"].replace("T", " ")[:16]
        topic = item["topic"][:20]
        fname = item["filename"][:20]

        print(f"{item['type']:<10} {topic:<25} {fname:<25} {time}")


# ─── MAIN MENU ─────────────────────────

def main():
    header()

    while True:
        print(f"\n{DIM}Menu:{RESET}")
        print(f"  {CYAN}1{RESET}. Generate file")
        print(f"  {CYAN}2{RESET}. Chat")
        print(f"  {CYAN}3{RESET}. View history")
        print(f"  {CYAN}q{RESET}. Quit")

        choice = input(f"\n{DIM}Choice:{RESET} ").strip().lower()

        if choice == "1":
            menu_generate()
        elif choice == "2":
            menu_chat()
        elif choice == "3":
            menu_history()
        elif choice == "q":
            print(f"\n{DIM}Goodbye!{RESET}")
            sys.exit(0)
        else:
            print(f"{RED}Invalid choice{RESET}")


# ─── RUN ───────────────────────────────

if __name__ == "__main__":
    main()