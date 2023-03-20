import scanner
from scanner import *


if __name__ == '__main__':
    scanner.init_symbol_table()
    Scanner("input.txt").scan_tokens()
    scanner.save_errors()
    scanner.save_tokens()
    scanner.save_symbol_table()