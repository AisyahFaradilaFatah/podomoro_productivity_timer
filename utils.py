"""
Utility functions untuk UI, input handling
"""

import os
from config import Colors, WELCOME_MESSAGE, AVAILABLE_COMMANDS

# TERMINAL UI FUNCTIONS
def clear_terminal() -> None:
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome() -> None:
    """Print welcome banner"""
    print(WELCOME_MESSAGE)
    print(AVAILABLE_COMMANDS)

def print_separator(char: str = "=", length: int = 60) -> None:
    """Print separator line"""
    print(char * length)

def print_success(message: str) -> None:
    """Print success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")

def print_error(message: str) -> None:
    """Print error message"""
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")

def print_warning(message: str) -> None:
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️ {message}{Colors.RESET}")

def print_info(message: str) -> None:
    """Print info message"""
    print(f"{Colors.CYAN}ℹ️ {message}{Colors.RESET}")

def print_user_input(text: str = "") -> str:
    """
    Print user input prompt dengan styling
    Args:
        text (str): Custom prompt text
    Returns:
        str: User input
    """
    prompt = f"{Colors.GREEN}📝 Kamu:{Colors.RESET} "
    return input(prompt)

def print_response(response: str) -> None:
    """
    Print assistant response dengan styling
    Args:
        response (str): Response text
    """
    print(f"{Colors.CYAN}🤖 Assistant:{Colors.RESET} {response}\n")

def print_goodbye() -> None:
    """Print goodbye message"""
    print(f"\n{Colors.YELLOW}👋 Selamat tinggal! Lanjut lagi besok ya! Tetap produktif! 🚀{Colors.RESET}")
    print(f"{Colors.YELLOW} Aisyah Faradila Fatah 2308292 MKB 5A {Colors.RESET}\n")

def handle_interrupt() -> None:
    """Handle Ctrl+C gracefully"""
    print(f"\n{Colors.YELLOW}⚠️ Interrupted. Ketik 'exit' untuk keluar.{Colors.RESET}\n")
