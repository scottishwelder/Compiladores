from json import load as j_load


class Tape:
    def __init__(self):
        self.position = 0
        with open("code") as file:
            self.string = file.read()

    def step(self):
        if self.position == len(self.string):
            return None
        self.position += 1
        return self.string[self.position - 1]

    def go_back(self):
        self.position -= 1


class Lexer:
    def __init__(self):
        self.tape = Tape()
        self.position = {'x': 0, 'y': 0}
        self.ids = []
        self.literals = []
        with open("automaton.json") as file:
            self.file = j_load(file)
        self.current_lexeme = ""
        self.currentState = self.file["initialState"]

    def reset(self):
        self.currentState = self.file["initialState"]
        self.current_lexeme = ""

    def __iter__(self):
        while True:
            symbol = self.tape.step()
            if symbol is None:
                if self.currentState == self.file["initialState"]:
                    return
                else:
                    raise Exception(
                        f"Erro léxico. Fim de arquivo inesperado: linha {self.position['y']}, posição {self.position['x']}")

            try:
                self.currentState = self.file["delta"][self.currentState][symbol]
            except KeyError:
                raise Exception(
                    f"Erro léxico. Símbolo inesperado: linha {self.position['y']}, posição {self.position['x']}")

            self.current_lexeme += symbol
            self.position['x'] += 1
            if symbol == '\n':
                self.position['y'] += 1
                self.position['x'] = 0

            final_state = self.file["finalStates"].get(self.currentState)
            if final_state:
                if final_state.get('lookahead'):
                    self.tape.go_back()
                lexeme = self.current_lexeme
                self.reset()
                table = final_state.get('table')
                if table:
                    if table == 'literal':
                        if lexeme in self.literals:
                            index = self.literals.index(lexeme)
                        else:
                            index = len(self.literals)
                            self.literals.append(lexeme)
                    elif table == 'id':
                        if lexeme in self.ids:
                            index = self.ids.index(lexeme)
                        else:
                            index = len(self.ids)
                            self.literals.append(lexeme)
                    else:
                        raise Exception('Autômato mal formado')
                    yield {'token': final_state['token'], 'lexeme': lexeme, 'table_index': index}
                else:
                    yield {'token': final_state['token'], 'lexeme': lexeme}
