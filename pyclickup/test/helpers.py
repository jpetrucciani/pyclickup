"""
helpers for the pytest suite
"""
import json
import sys
from colorama import init, Fore, Style


init()


def dbg(text: str) -> None:
    """debug printer for tests"""
    if isinstance(text, dict):
        text = json.dumps(text, sort_keys=True, indent=2)
    caller = sys._getframe(1)
    print("")
    print(Fore.GREEN + Style.BRIGHT)
    print("----- {} line {} ------".format(caller.f_code.co_name, caller.f_lineno))
    print(text)
    print("-----")
    print(Style.RESET_ALL)
    print("")
