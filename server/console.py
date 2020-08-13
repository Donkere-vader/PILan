import os
import platform
import datetime

LOGO = """\033[31m
██████╗ ██╗██╗      █████╗ ███╗   ██╗
██╔══██╗██║██║     ██╔══██╗████╗  ██║
██████╔╝██║██║     ███████║██╔██╗ ██║
██╔═══╝ ██║██║     ██╔══██║██║╚██╗██║
██║     ██║███████╗██║  ██║██║ ╚████║
╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝
\033[0m"""

class Console:
    """ Class used for a beautifull terminal output """
    def __init__(self):
        self._log = []
        self.output()

    def clear_screen(self):
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    def output(self):
        self.clear_screen()

        print(LOGO)

        for item in self._log[-20:]:
            print(item)

    def log(self, txt, negative=False):
        color_code = "\033[7;32m"
        if negative:
            color_code = "\033[7;31m"

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        log_item = f"{color_code}[{timestamp}]\033[0;0m {txt}"
        self._log.append(log_item)
        self.output()

    def input(self, txt):
        _inpt = input(txt)

        self.log(txt + _inpt)
        return _inpt