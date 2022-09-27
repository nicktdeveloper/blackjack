""" Module for printing in color """
import colorama
from colorama import Fore, Back, Style

colorama.init()

print(Fore.RED + 'some red text')
print('some text')