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


class Lexer:
    def __init__(self):
        self.tape = Tape()
        self.position = [0, 0]
        self.lexem = ""
        with open("automaton.json") as file:
            self.file = j_load(file)
        self.currentState = self.file["initialState"]

    def reset(self):
        self.currentState = self.file["initialState"]
        self.lexem = ""

    def step(self, symbol):
        self.position[1] += 1
        if symbol == '\n':
            self.position[0] += 1
        self.lexem += symbol
        try:
            self.currentState = self.file["delta"][self.currentState][symbol]
        except KeyError:
            raise Exception(f"Erro léxico. Símbolo inesperado: linha {self.position[0]}, posição {self.position[1]}")

    def __iter__(self):
        while True:
            symbol = self.tape.step()
            if symbol is None:
                if self.currentState == self.file["initialState"]:
                    return
                else:
                    raise Exception(f"Erro léxico. Fim de arquivo inesperado: linha {self.position[0]}, posição {self.position[1]}")
            self.step(symbol)
            final_state = self.file["finalStates"].get(self.currentState)
            if final_state:
                lexem = self.lexem
                self.reset()
                yield final_state, lexem
