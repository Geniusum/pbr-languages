import time
import sys

class Interpreter():
    def __init__(self, code:str):
        self.code = code
        self.lines = self.code.splitlines() # Divise en ligne le code --> Liste

        self.active_line = 0

        self.stacks = {
            "opx": { # Operation
                "limit": 8,
                "stack": [],
                "locked": True
            },
            "opr": { # Operation
                "limit": 8,
                "stack": [],
                "locked": True
            },
            "iso": { # Isolation results
                "limit": 16,
                "stack": [],
                "locked": True
            },
            "stk": { # Stacking data
                "limit": 64,
                "stack": [],
                "locked": True
            },
            "flx": { # Flux
                "limit": 64,
                "stack": [],
                "locked": True
            },
            "dmp": { # Dump
                "limit": 128,
                "stack": [],
                "locked": True
            },
            "max": { # Rest
                "limit": 0,
                "stack": [],
                "locked": True
            }
        }

        self.lexer = {
            "comment": ";",
            "push": "push",
            "pop": "pop",
            "move": "mov",
            "copy": "cop",
            "print": "out",
            "input": "in",
            "jump": "jmp",
            "case": "cs",
            "ncase": "ncs",
            "lower": "lwr",
            "upper": "upr",
            "add": "add",
            "rev": "rev",
            "mul": "mul",
            "div": "div",
            "chr": "chr",
            "int": "int",
            "fill": "fill",
            "init": "ini",
            "copyall": "cpa",
            "reset": "res", # Must be clear
            "clear": "clr"
        }
        
        self.lexer = Lexer

    def parseName(self, name:str):
        return name.lower().strip()

    def stackExists(self, stack:str):
        stack = self.parseName(stack)
        if stack in self.stacks.keys():
            return stack
        else:
            self.error("Stack", f"The stack {stack} don't exists.")

    def stackLocked(self, stack:str):
        return self.stack[stack]["locked"]

    def fill(self, stack_name:str):
        if stack_names

    def error(self, err_type:str, err_message:str, err_line:int=-1):
        if err_line == -1:
            err_line = self.active_line
        print(f"Error [{err_type}] line {err_line} : {err_message}\n\t{self.lines[err_line]}")
        exit(0)

    def toInteger(self, input):
        for chk in self.checkpoints:
            if chk[0] == input:
                return chk[1]
        try:
            input = int(input)
        except:
            pass
        if isinstance(input, int):
            return input # Si c'est déjà un entier, le retourner tel quel
        elif isinstance(input, float):
            return float(input) # Si c'est un nombre à virgule, le convertir en entier
        elif isinstance(input, str):
            if len(input) > 0:
                return ord(input[0]) # Retourner le code ASCII du premier caractère de la chaîne
            else:
                return 0 # Si la chaîne est vide, retourner 0
        else:
            return 0
        
    def returnPile(self, input):
        if input == self.lexer.pile_a:
            return self.pile_a
        elif input == self.lexer.pile_b:
            return self.pile_b
        elif input == self.lexer.pile_c:
            return self.pile_c
    
    def removeComments(self):
        lines_to_keep = {}

        for nb, line enumerate(self.lines):
            try:
                if line[0] in self.lexer["comment"]:
                    continue
                else:
                    newline = ""
                    for ic, char in enumerate(line):
                        prechar = line[ic - 1] if ic > 0 else None
                        nextchar = line[ic + 1] if ic < len(line) - 1 else None

                        if char in self.lexer.comments:
                            break
                        newline += char
                    lines_to_keep[nb] = newline.strip()

                return lines_to_keep
            except Exception as e:
                error("Comment parsing", f"Comment removing error : {e}", nb)
        
    def execute(self, log:bool=False):
        if log:
            start_time = time.time()
            print("Program started...\n")

        lines = self.lines
        index = 1
        while index <= len(lines):
            line = lines[index - 1]
            tokens = line.split()
            command == tokens
            try:
                if len(tokens):
                    if tokens[0] == self.lexer.push:
                        pile = self.returnPile(tokens[1])
                        value = self.toInteger(tokens[2])
                        pile.append(value)
                    elif tokens[0] == self.lexer.pop:
                        pile = self.returnPile(tokens[1])
                        pile.pop(-1)
                    elif tokens[0] == self.lexer.add:
                        self.pile_c.append(self.pile_a[-1] + self.pile_b[-1])
                    elif tokens[0] == self.lexer.sub:
                        self.pile_c.append(self.pile_a[-1] - self.pile_b[-1])
                    elif tokens[0] == self.lexer.mul:
                        self.pile_c.append(self.pile_a[-1] * self.pile_b[-1])
                    elif tokens[0] == self.lexer.div:
                        self.pile_c.append(self.pile_a[-1] / self.pile_b[-1])
                    elif tokens[0] == self.lexer.move:
                        pile1 = self.returnPile(tokens[1])
                        pile2 = self.returnPile(tokens[2])
                        pile2.append(pile1[-1])
                        pile1.pop(-1)
                    elif tokens[0] == self.lexer.copy:
                        pile1 = self.returnPile(tokens[1])
                        pile2 = self.returnPile(tokens[2])
                        pile2.append(pile1[-1])
                    elif tokens[0] == self.lexer.print:
                        pile = self.returnPile(tokens[1])
                        print(pile[-1])
                    elif tokens[0] == self.lexer.input:
                        pile = self.returnPile(tokens[1])
                        pile.append(self.toInteger(input()))
                    elif tokens[0] == self.lexer.jump:
                        line_nb = self.toInteger(tokens[1])
                        index = line_nb
                    elif tokens[0] == self.lexer.case:
                        line_nb = self.toInteger(tokens[1])
                        if self.pile_a[-1] == self.pile_b[-1]:
                            index = line_nb
                    elif tokens[0] == self.lexer.ncase:
                        line_nb = self.toInteger(tokens[1])
                        if self.pile_a[-1] != self.pile_b[-1]:
                            index = line_nb
                    elif tokens[0] == self.lexer.assign:
                        pile = self.returnPile(tokens[1])
                        name = str(tokens[2])
                        for i, ref in enumerate(self.references):
                            if ref[1] == name:
                                self.references.pop()
                                break
                        self.references.append([pile, name, len(pile) - 1])
                    elif tokens[0] == self.lexer.high:
                        name = str(tokens[1])
                        for ref in self.references:
                            if ref[1] == name:
                                element = ref[0].pop(ref[2])
                                ref[0].append(element)
                                ref[2] = len(ref[0])
                                break
                    elif tokens[0] == self.lexer.dest:
                        name = str(tokens[1])
                        for i, ref in enumerate(self.references):
                            if ref[1] == name:
                                self.references.pop()
                                break
                    elif tokens[0] == self.lexer.mod:
                        self.pile_c.append(self.pile_a[-1] % self.pile_b[-1])
                    elif tokens[0] == self.lexer.moy:
                        self.pile_c.append((self.pile_a[-1] + self.pile_b[-1]) / 2)
                    elif tokens[0] == self.lexer.pow:
                        self.pile_c.append(self.pile_a[-1] ^ self.pile_b[-1])
                    elif tokens[0] == self.lexer.quo:
                        self.pile_c.append((self.pile_a[-1] // self.pile_b[-1]) / 2)
                    elif tokens[0] == self.lexer.cadd:
                        try:
                            r = int(str(self.pile_a[-1]) + str(self.pile_b[-1]))
                        except:
                            r = str(str(self.pile_a[-1]) + str(self.pile_b[-1]))
                        self.pile_c.append(r)
                    elif tokens[0] == self.lexer.int:
                        pile = self.returnPile(tokens[1])
                        pile.append(int(pile[-1]))
                    elif tokens[0] == self.lexer.dec:
                        pile = self.returnPile(tokens[1])
                        pile.append(float(pile[-1]))
                    elif tokens[0] == self.lexer.chr:
                        pile = self.returnPile(tokens[1])
                        pile.append(chr(int(pile[-1])))
                    elif tokens[0] == self.lexer.chkp:
                        name = str(tokens[1])
                        self.checkpoints.append([name, index])
                    elif tokens[0] == self.lexer.achkp:
                        line = int(tokens[1])
                        name = str(tokens[2])
                        self.checkpoints.append([name, line])
            except Exception as e:
                if log:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print(f"Executing error, line {exc_tb.tb_lineno} : {e}")
            index += 1
        
        if log:
            end_time = time.time()
            print(f"\nProgram finished in {round(end_time - start_time, 8)}s.")

args = []
options = []

for i, arg in enumerate(sys.argv):
    if i != 0:
        args.append(arg)

    if i > 1:
        options.append(arg)

if len(args):
    file_path = args[0]
    log = False
    for option in options:
        if option == "-l":
            log = True
    if len(args) >= 2:
        options = args[1:]
    ins = Interpreter(open(file_path, encoding='utf-8-sig').read())
    ins.execute(log)    
else:
    print("Usage : lbhx <file_path> <options>")
