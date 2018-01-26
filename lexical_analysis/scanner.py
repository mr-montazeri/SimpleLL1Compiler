import re

# Token separator does not contain EOF, so the last line of code should be empty (or we should handle it somehow)
from lexical_analysis.token import Token

TOKEN_SEPARATOR_REGEX = r'(?=[\-+/*&|=<>(){},:;.]|\s)'

TOKENS_REGEX_OBJECT = re.compile('(?P<PUBLIC>public{separator})' \
                                 r'|(?P<CLASS>class{separator})' \
                                 r'|(?P<STATIC>static{separator})' \
                                 r'|(?P<VOID>void{separator})' \
                                 r'|(?P<MAIN>main{separator})' \
                                 r'|(?P<EXTENDS>extends{separator})' \
                                 r'|(?P<RETURN>return{separator})' \
                                 r'|(?P<BOOLEAN>boolean{separator})' \
                                 r'|(?P<INT>int{separator})' \
                                 r'|(?P<IF>if{separator})' \
                                 r'|(?P<ELSE>else{separator})' \
                                 r'|(?P<WHILE>while{separator})' \
                                 r'|(?P<FOR>for{separator})' \
                                 r'|(?P<PRINT>System\.out\.println{separator})' \
                                 r'|(?P<TRUE>true{separator})' \
                                 r'|(?P<FALSE>false{separator})' \
                                 r'|(?P<MINUS>-(?=[\sa-zA-Z()]))' \
                                 r'|(?P<PLUS>\+(?=[\sa-zA-Z()]))' \
                                 r'|(?P<LINECOMMENT>//)' \
                                 r'|(?P<BLCKCOMMENT>/\*)' \
                                 r'|(?P<DIVIDE>/)' \
                                 r'|(?P<MULTIPLY>\*)' \
                                 r'|(?P<AND>&&)' \
                                 r'|(?P<OR>\|\|)' \
                                 r'|(?P<EQUAL>==)' \
                                 r'|(?P<SETVAL>=)' \
                                 r'|(?P<PLSETVAL>\+=)' \
                                 r'|(?P<LT><)' \
                                 r'|(?P<RPAREN>\()' \
                                 r'|(?P<LPAREN>\))' \
                                 r'|(?P<LBRACE>{{)' \
                                 r'|(?P<RBRACE>}})' \
                                 r'|(?P<COMMA>,)' \
                                 r'|(?P<SEMICOLON>;)' \
                                 r'|(?P<DOT>\.)' \
                                 r'|(?P<LITERAL>[+\-]?\d+{separator})' \
                                 r'|(?P<IDENTIFIER>[a-zA-Z][0-9a-zA-Z]*{separator})' \
                                 r'|(?P<SPACES>\s+)' \
                                 r''.format(separator=TOKEN_SEPARATOR_REGEX))
NEWLINE_CHARACTER = '\n'

class Scanner:
    ignored_tokens = ['SPACES']

    def __init__(self, text):
        self.text = text
        self.start = 0

    def tokens(self):
        while self.start < len(self.text):
            match = TOKENS_REGEX_OBJECT.match(self.text, self.start)
            if match:
                name, lexeme = next(filter(
                    lambda x: x[1] is not None,
                    match.groupdict().items()
                ))

                if name == 'LINECOMMENT':
                    self.skip_comments(NEWLINE_CHARACTER)
                elif name == 'BLCKCOMMENT':
                    self.skip_comments('*/')
                else:
                    self.seek_to(self.start + len(lexeme))
                    if name not in self.ignored_tokens:
                        yield Token(lexeme, name)
            else:
                self.handle_lexical_error('Unexpected string')

    def seek_to(self, dest):
        self.start = dest

    def skip_comments(self, ending):
        ending_pos = self.text.find(ending, self.start)
        skip_to = self.start
        if ending_pos == -1:
            if ending == NEWLINE_CHARACTER:
                skip_to = len(self.text)
            else:
                self.handle_lexical_error('Comment block left open!')
        else:
            skip_to = ending_pos + len(ending)
        self.seek_to(skip_to)

    def handle_lexical_error(self, error_message):
        raise Exception(error_message)
