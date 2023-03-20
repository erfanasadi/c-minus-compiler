import scanner
from scanner import *


if __name__ == '__main__':
    Scanner("input.txt").scan_tokens()
    scanner.save_errors()
    scanner.save_tokens()