import rud
import os

script_path = os.path.dirname(os.path.abspath(__file__))

def stklen(self: rud.Interpreter, args:list[str]):
    stack_name = self.stackInitialized(self.stackExists(args[0]))
    out_stack = self.stackInitialized(self.stackExists("iso"))
    self.push(out_stack, len(self.getStackList(stack_name)))

def execute(self: rud.Interpreter, args:list[str]):
    for arg in args:
        arg = arg.replace("/", "\\")
        if arg.startswith("*") and arg.endswith("*"):
            arg = arg[1:-1]
            path = os.path.join(script_path, "libs", arg)
        else:
            path = arg
        content = open(path).read()
        newintr = rud.Interpreter(content)
        newintr.execute(False, False)

def include(self: rud.Interpreter, args:list[str]):
    for arg in args:
        arg = arg.replace("/", "\\")
        if arg.startswith("*") and arg.endswith("*"):
            arg = arg[1:-1]
            path = os.path.join(script_path, "libs", arg)
        else:
            path = arg
        content = open(path).read()
        newintr = rud.Interpreter(content)
        newintr.execute(False, False)

names = {
    "stklen": stklen,
    "execute": execute,
    "include": include
}