from enum import Enum
import keyword


class TokenType(Enum):
    LEFT_PAREN = '('
    RIGHT_PAREN=')'
    LEFT_CURLY='{'
    RIGHT_CURLY = '}'
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    DOUBLE_QUOTED_STRING = 'DB_STR'
    SINGLE_QUOTED_STRING = 'SL_STR'
    COMMENT = '#'
    COMMA = ','
    ASTERISK = "*"
    COLON =":"
    NUMBER = "NUMBER"
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    SPACE = "SPACE"
    INVALID = "INVALID"


class LEX_PYTHON:
    def __init__(self, in_str):
        self.program = in_str
        self.index = 0
        self.tokens = []

    def peek(self, offset = 0):
        return self.program[self.index + offset]

    def consume(self):
        char = self.program[self.index]
        self.index += 1
        return char


    def emit_token(self, token_type):
        self.tokens.append(token_type)
        print(token_type)
        self.index += 1

    def commit_token(self, token_type):
        self.tokens.append(token_type)
        print(token_type)

    def is_valid_first_character_of_identifier(self, ch):
        return ch.isalpha() or ch == '_'


    def is_valid_nonfirst_character_of_identifier(self, ch):
        return self.is_valid_first_character_of_identifier(ch) or ch.isnumeric()

    def lex(self):

        while self.index < len(self.program):
            #import pdb;pdb.set_trace();
            print(self.index, len(self.program))
        
            ch = self.peek()
            
            if ch == ":":
                self.emit_token(TokenType.COLON)
            elif ch == "*":
                self.emit_token(TokenType.ASTERISK)
            elif ch == ',':
                self.emit_token(TokenType.COMMA)
            elif ch == '(':
               self.emit_token(TokenType.LEFT_PAREN)
            elif ch == ')':
                self.emit_token(TokenType.RIGHT_PAREN)
            elif ch == '{':
                self.emit_token(TokenType.LEFT_CURLY)
            elif ch == '}':
                self.emit_token(TokenType.RIGHT_CURLY)
            elif ch == '[':
                self.emit_token(TokenType.LEFT_BRACKET)
            elif ch == ']':
                self.emit_token(TokenType.RIGHT_BRACKET)
            elif ch == '"':
                self.emit_token(TokenType.DOUBLE_QUOTED_STRING)
            elif ch == "'":
                self.emit_token(TokenType.SINGLE_QUOTED_STRING)
            elif ch == " ":
                self.emit_token(TokenType.SPACE)
            
            elif ch.isnumeric():
                #begin_token()
                while(self.peek() and self.peek().isnumeric()):
                    self.consume()
                self.commit_token(TokenType.NUMBER)
                continue

            elif self.is_valid_first_character_of_identifier(ch):
                start_idx = self.index
                while self.peek() and self.is_valid_nonfirst_character_of_identifier(self.peek()):
                    self.consume()
                end_idx = self.index
                print(start_idx, end_idx)
                ss = self.program[start_idx:end_idx]
                print("GOT VIEW: ", ss)
                    
                if keyword.iskeyword(ss):
                    self.commit_token(TokenType.KEYWORD)
                else:
                    self.commit_token(TokenType.IDENTIFIER)

                continue

            else:
                self.emit_token(TokenType.INVALID)
            #if ch == "#":
            #    while self.peek():
            #        if self.consume == '\n':
            #            break
            #    continue

        return self.tokens




