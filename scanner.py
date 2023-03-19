symbol_table = dict()
lexical_errors = list()
tokens = list()


class TokenType:
    SYMBOL = 'SYMBOL'
    NUM = 'NUM'
    ID = 'ID'
    KEYWORD = 'KEYWORD'
    COMMENT = 'COMMENT'
    WHITESPACE = 'WHITESPACE'
    ID_OR_KEYWORD = 'ID_OR_KEYWORD'
    INVALID = 'Invalid input'


class Scanner:
    def __init__(self, input_path):
        self.input_path = input_path
        self.selflines = None

        self.line_number = 0
        self.cursor = 0

    def get_next_token(self):
        if self.eof_reached():
            return False
        char = self.get_current_char()
        token_type = self.get_token_type(char)

    def eof_reached(self):
        return self.cursor >= len(self.lines)

    def scan_tokens(self):
        with open(self.input_path, 'r') as f:
            self.lines = ''.join([line for line in f.readlines()])

        while True:
            if self.eof_reached():
                break
            token = self.get_next_token()
            if token:
                tokens[token[0]].append(token[1:])

    def get_current_char(self):
        return self.lines[self.cursor]

    def get_token_type(char):
        if char in [' ', '\t', '\n', '\r', '\v', '\f']:  # WHITESPACE
            return TokenType.WHITESPACE
        elif char in [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<']:  # SYMBOL
            return TokenType.SYMBOL
        elif char.isdigit():  # NUM
            return TokenType.NUM
        elif char.isalnum():  # ID / KEYWORD
            return TokenType.ID_OR_KEYWORD
        elif char == '/':  # COMMENT (potentially)
            return TokenType.COMMENT
        else:  # Invalid input
            return TokenType.INVALID