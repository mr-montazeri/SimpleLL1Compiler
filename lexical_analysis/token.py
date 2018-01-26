class Token:
    def __init__(self, lexeme, token_name):
        self.lexeme = lexeme
        self.token_name = token_name

    @property
    def value(self):
        if self.token_name == 'LITERAL':
            return int(self.lexeme)
        if self.token_name == 'IDENTIFIER':
            return self.lexeme
        return None

    def __str__(self):
        parts = [self.token_name]
        if self.value is not None:
            parts.append(str(self.value))
        return '({})'.format(
            ', '.join(parts)
        )
