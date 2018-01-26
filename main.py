from lexical_analysis.scanner import Scanner

if __name__ == '__main__':
    code = open('code.mjava')
    scanner = Scanner(code.read())
    for token in scanner.tokens():
        print(token)
