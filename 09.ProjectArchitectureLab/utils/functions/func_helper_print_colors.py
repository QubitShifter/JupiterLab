from colorama import init, Fore, Style

init(autoreset=True)

PRINT_COLOR_CONFIG ={
    'info': Fore.CYAN,
    'debug': Fore.BLUE,
    'success': Fore.GREEN,
    'error': Fore.RED,
    'highlight': Fore.MAGENTA,
    'warning': Fore.YELLOW,
    'default': Fore.WHITE
}


def color_print(text, level='info', indent="   "):
    color = PRINT_COLOR_CONFIG.get(level.lower(), Fore.WHITE)
    print(color + indent + str(text) + Style.RESET_ALL)
