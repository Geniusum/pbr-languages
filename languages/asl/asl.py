import time
import sys

class Interpreter():
    def __init__(self, code:str, path:str):
        self.code = code
        self.path = path
        self.lines = {}
        for nb, line in enumerate(self.code.splitlines()):
            self.lines[nb] = line

        self.references = []
        self.checkpoints = []
        
        self.act_adr = 0

        self.lexer = {
            "comments": ";",
            "commands": {"push": self._push, "pop": self._pop, "move": self._move, "copy": self._copy, "print": self._print, "input": self._input,
                         "add": self._add, "sub": self._sub, "mul": self._mul,
                         "div": self.v, "assign": self.v, "high": self.v, "dest": self.v, "mod": self.v, "moy": self.v,
                         "pow": self.v, "quo": self.v, "cadd": self.v, "int": self.v, "dec": self.v, "chr": self.v,
                         "pil": self.v, "del": self.v, "init": self.v, "plan": self.v, "str": self.v,
                         "strid": self.v, "section": self.v, "call": self.v, "dub": self.v, "import": self.v,
                         "inject": self.v, "initall": self.v, "fil": self.v, "is": self.v, "not": self.v, "more": self.v,
                         "less": self.v, "and": self.v, "or": self.v, "bool": self.v, "adr": self.v, "toint": self.v,
                         "todec": self.v, "tobool": self.v, "tochr": self.v, "toadr": self.v, "end": self.v,
                         "endstr": self.v, "return": self.v, "todo": self.v}
        }

        self.stack_types = {
            "pile": -1,
            "file": 0
        }

        self.stacks = {
            "stored": {
                "type": "pile",
                "address": self.getNewAddress(),
                "stack": [],
                "lenght": 0,
                "protected": True,
                "initialised": False
            },
            "strings": {
                "type": "pile",
                "address": self.getNewAddress(),
                "stack": [],
                "lenght": 0,
                "protected": True,
                "initialised": False
            },
            "results": {
                "type": "pile",
                "address": self.getNewAddress(),
                "stack": [],
                "lenght": 0,
                "protected": True,
                "initialised": False
            },
            "one": {
                "type": "pile",
                "address": self.getNewAddress(),
                "stack": [],
                "lenght": 0,
                "protected": True,
                "initialised": False
            },
            "two": {
                "type": "pile",
                "address": self.getNewAddress(),
                "stack": [],
                "lenght": 0,
                "protected": True,
                "initialised": False
            }
        }

        self.sections = {}
        
        self.error_ = False

        self.removeComments()

    def v(self, *args):
        pass

    def getNewAddress(self):
        self.act_adr += 1
        return hex(int(self.act_adr))
    
    def error(self, line:int, line_content:str, error:str):
        print(f"Error line {line + 1} : {line_content}\n\tException : {error}")
        self.error_ = True

    def _push(self, line:int, line_content:str, *args):
        values = []
        stacks = ["stored"]
        for arg in args:
            j = self.parseBExp(arg, line, line_content)
            if j["type"] == "stack":
                stacks.append(j["value"])
            else:
                values.append(j["value"])
        for stack in stacks:
            stack = self.stacks[stack]
            if len(stack["stack"]) >= stack["lenght"] and not stack["lenght"] <= 0:
                while not len(stack["stack"]) < stack["lenght"]:
                    stack["stack"].pop(self.stack_types[stack["type"]])
            stack["stack"] += values
    
    def _pop(self, line:int, line_content:str, *args):
        stacks = args
        for stack_ in stacks:
            stack = self.stacks[self.parseBExp(stack_, line, line_content)["value"]]
            try:
                stack["stack"].pop()
            except:
                self.error(line, line_content, f"The stack {stack_} is already empty.")

    def _add(self, line:int, line_content:str, *args):
        stacks = args
        for stack in stacks:
            stack = self.stacks[self.parseBExp(stack, line, line_content)["value"]]["stack"]
            try:
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
            except:
                self.error(line, line_content, f"The stack don't have the minimum items number.")

    def _sub(self, line:int, line_content:str, *args):
        stacks = args
        for stack in stacks:
            stack = self.stacks[self.parseBExp(stack, line, line_content)["value"]]["stack"]
            try:
                b = stack.pop()
                a = stack.pop()
                stack.append(a - b)
            except:
                self.error(line, line_content, f"The stack don't have the minimum items number.")

    def _mul(self, line:int, line_content:str, *args):
        stacks = args
        for stack in stacks:
            stack = self.stacks[self.parseBExp(stack, line, line_content)["value"]]["stack"]
            try:
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)
            except:
                self.error(line, line_content, f"The stack don't have the minimum items number.")

    def _div(self, line:int, line_content:str, *args):
        stacks = args
        for stack in stacks:
            stack = self.stacks[self.parseBExp(stack, line, line_content)["value"]]["stack"]
            try:
                b = stack.pop()
                a = stack.pop()
                stack.append(a / b)
            except:
                self.error(line, line_content, f"The stack don't have the minimum items number.")

    def _move(self, line:int, line_content:str, *args):
        stack_a, stack_b = self.stacks[self.parseBExp(args[0], line, line_content)["value"]]["stack"], self.stacks[self.parseBExp(args[1], line, line_content)["value"]]["stack"]
        stack_b.append(stack_a.pop())
    
    def _copy(self, line:int, line_content:str, *args):
        stack_a, stack_b = self.stacks[self.parseBExp(args[0], line, line_content)["value"]]["stack"], self.stacks[self.parseBExp(args[1], line, line_content)["value"]]["stack"]
        stack_b.append(stack_a[-1])
    
    def _print(self, line:int, line_content:str, *args):
        stacks = args
        for stack in stacks:
            stack = self.stacks[self.parseBExp(stack, line, line_content)["value"]]
            print(stack)
    
    def _input(self, line:int, line_content:str, *args):
        stacks = args
        for stack in stacks:
            stack = self.stacks[self.parseBExp(stack, line, line_content)["value"]]["stack"]
            stack.append(self.parseBExp(input(), line, line_content)["value"])

    def parseBExp(self, input, line:int, line_content:str):
        try:
            for chk in self.checkpoints:
                if chk[0] == input:
                    return chk[1]
            type = "int"
            nb = [*"0123456789"]
            commas = [*".,"]
            for char in str(input):
                if not char in nb and type == "int":
                    d = char.replace(commas[0], "").replace(commas[1], "")
                    d_type = "dec"
                    for d_char in d:
                        if not char in nb and d_type == "dec":
                            d_type = "str"
                    type = d_type
            if len(input) >= 2:
                if input[:2] == "0x":
                    type = "adr"
            if str(input).lower() == "true":
                type = "bool"
                input = True
            elif str(input).lower() == "false":
                type = "bool"
                input = False
                
            if type == "int":
                return {
                    "type": type,
                    "value": int(input)
                }
            elif type == "dec":
                return {
                    "type": type,
                    "value": float(input)
                }
            elif type == "str":
                if str(input).lower() in self.stacks:
                    type = "stack"
                    stack = str(input).lower()
                    return {
                        "type": type,
                        "value": stack
                    }
                if len(input) > 0:
                    return {
                        "type": type,
                        "value": ord(input[0])
                    }
                else:
                    return {
                        "type": type,
                        "value": 0
                    }
            elif type == "bool":
                return {
                    "type": type,
                    "value": input
                }
            elif type == "adr":
                return {
                    "type": type,
                    "value": hex(input)
                }
            else:
                self.error()
                return {
                    type: None,
                    "value": 0
                }
        except Exception as e:
            self.error(line, line_content, f"Error in typing : {e}")

    def makeName(self, input:str, line:int, line_content:str):
        input = str(input).upper()
        if input[0] in [*"0123456789"]:
            self.error(line, line_content, f"The section name '{input}' can't start with a number.")
        not_valid = False
        chars = "abcdefghijklmnopqrstuvwxyz"
        chars += chars.upper()
        chars += "0123456789_"
        chars = [*chars]
        for char in input:
            if not char in chars:
                not_valid = True
        if not_valid:
            self.error(line, line_content, f"The section name '{input}' has invalid character(s).")
        if input in self.sections.keys() or input in self.stacks.keys():
            self.error(line, line_content, f"The section '{input}' already exists in section or stacks .")
        
    def returnSection(self, input, line:int, line_content:str, f:bool=False):
        input = str(input).upper()
        if not f:
            if input.split(".")[0] in self.sections.keys():
                if len(input) > 1:
                    return self.returnSection(".".join(input.split()[1:]), True)
                else:
                    return self.sections[input]
            else:
                self.error(line, line_content, f"The section '{input}' don't exists.")
        else:
            if input.split(".")[0] in self.sections["after"].keys():
                if len(input) > 1:
                    return self.returnSection(".".join(input.split()[1:]), True)
                else:
                    return self.sections[input]
            else:
                self.error(line, line_content, f"The section '{input}' don't exists.")
    
    def removeComments(self):
        lines_to_keep = {}

        for nb, line in self.lines.items():
            try:
                if line[0] == self.lexer["comments"] and not (line.split()[0] == self.lexer["str"] or line.split()[0] == self.lexer["strid"]):
                    continue
                else:
                    newline = ""
                    for ic, char in enumerate(line):
                        prechar = line[ic - 1] if ic > 0 else None
                        nextchar = line[ic + 1] if ic < len(line) - 1 else None

                        if char == self.lexer["comments"]:
                            break
                        newline += char
                    lines_to_keep[nb] = newline.strip()

                self.lines = lines_to_keep
            except Exception as e:
                self.error(nb, line, f"Comments parsing error : {e}")

    def exec(self, line:int, line_content:str):
        tokens = line_content.split()
        if not tokens[0].lower() in self.lexer["commands"].keys():
            self.error(line, line_content, f"Syntax error, invalid command '{tokens[0]}'.")
        else:
            try:
                func = self.lexer["commands"][tokens[0].lower()]
                func(line, line_content, *tuple(tokens[1:]))
            except Exception as e:
                import traceback
                self.error(line, line_content, f"Error during command function execution (maybe due to a lack or overflow of command arguments) : {traceback.format_exc()}")

    def run(self, log:bool=False):
        if log:
            start_time = time.time()
            print("Program started...\n")

        lines = self.lines
        index = 1
        while index <= list(lines.keys())[-1] + 1:
            if not self.error_:
                if index - 1 in lines.keys():
                    line = index - 1
                    line_content = lines[line]
                    try:
                        if len(line_content.strip()):
                            self.exec(line, str(line_content).strip())
                            """if tokens[0] == self.lexer["push"]:
                                pile = self.returnPile(tokens[1])
                                value = self.toInteger(tokens[2])
                                pile.append(value)
                            elif tokens[0] == self.lexerpop:
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
                                self.checkpoints.append([name, line])"""
                    except Exception as e:
                        if log:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            self.error(line, line_content, f"Executing error, line {exc_tb.tb_lineno} : {e}")
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
    ins = Interpreter(open(file_path, encoding='utf-8-sig').read(), file_path)
    ins.run(log)
    print()
    print(ins.stacks)    
else:
    print("Usage : asl <file_path> <options>")