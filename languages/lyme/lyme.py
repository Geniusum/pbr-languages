import sys
args = sys.argv[1:]

def printUsage():
    print("Lyme, a programming language compiled in LBHX\nUsage : lyme <command> <path(s) / arg(s)>\n\nCommands :\n\trun <.lym file path> : compile and execute a Lyme program (output : <lym_file_name>.rud).\n\tcompile <.lym file path> : compile a Lyme program (output : <lym_file_name>.rud).")

if len(args):
    command = args[0]
    command_args = args[1:]
    if not len(command_args):
        printUsage()
else:
    printUsage()