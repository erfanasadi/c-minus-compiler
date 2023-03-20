from collections import defaultdict
symbol_table = dict()
lexical_errors = defaultdict(list)
tokens = defaultdict(list)



class TokenType:
    SYMBOL = 'SYMBOL'
    NUM = 'NUM'
    ID = 'ID'
    KEYWORD = 'KEYWORD'
    COMMENT = 'COMMENT'
    WHITESPACE = 'WHITESPACE'
    ID_OR_KEYWORD = 'ID_OR_KEYWORD'
    INVALID = 'Invalid input'


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


def save_errors():
     with open('lexical_errors.txt', 'w') as f:
        if lexical_errors:

            for line_num,line_eror in lexical_errors.items():
                f.write(f'{line_num+1}.'+"\t")
                for i in range(len(line_eror)):
                    if(i==len(line_eror)-1):
                        for char in range(len(line_eror[i])):
                            f.write(f'{line_eror[i][char]}')
                        f.write("\n")
                    else:
                        f.write(f'{line_eror[i]} ')
        else:
          print('There is no lexical error.')
    #   f.write('There is no lexical error.')

def save_tokens():
    with open('tokens.txt', 'w') as f:
        f.write('\n'.join([f'{line_no + 1}.\t' + ' '.join([f'({token[0]}, {token[1]})' for token in tokens])
                           for line_no, tokens in tokens.items()]))

class Scanner:
    def __init__(self, input_path):
        self.input_path = input_path
        self.selflines = None

        self.line_number = 0
        self.cursor = 0

    def scan_next_token(self):
        if self.eof_reached():
            return False
        char = self.get_current_char()
        token_type = get_token_type(char)
        if token_type == TokenType.WHITESPACE:
            if char == '\n':
                self.line_number += 1
            self.cursor += 1
            return self.scan_next_token()
        if token_type == TokenType.NUM:
            number, error = self.isnumber()
            if not error:
                return self.line_number, TokenType.NUM, number

            lexical_errors[self.line_number].append("(" + number + ", Invalid number)")

        else:
            self.cursor += 1

    def eof_reached(self):
        return self.cursor >= len(self.lines)

    def scan_tokens(self):
        with open(self.input_path, 'r') as f:
            self.lines = ''.join([line for line in f.readlines()])

        while True:
            if self.eof_reached():
                break
            token = self.scan_next_token()
            if token:
                tokens[token[0]].append(token[1:])

    def get_current_char(self):
        return self.lines[self.cursor]

    def isnumber(self):
        num = self.get_current_char()
        while self.cursor + 1 < len(self.lines):
            self.cursor += 1
            next_char = self.get_current_char()
            temp_type = get_token_type(next_char)

            if temp_type == TokenType.NUM:
                num += next_char
            elif temp_type == TokenType.WHITESPACE or temp_type == TokenType.SYMBOL:
                self.cursor += 1
                return num, False
            else:  # invalid num
                num += next_char
                self.cursor += 1
                return num, True

        self.cursor += 1
        return num, False
