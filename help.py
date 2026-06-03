from tools.registry import TOOLS

def help(ai_name):
        print(f"{ai_name}: Available commands:")
        print()
        for tool in TOOLS:
                print(tool)
                print()
