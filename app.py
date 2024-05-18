import os
import sys
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

folder = config.get("General", "file_loc")

def print_help():
    print("Python Todo.txt Help")
    sys.exit()

def get_action(args):
    if len(args) <= 1:
        print_help()
    else:
        action = args[1]
        return action
    return

def get_list_of_lines_in_file(folder_loc):
    file_loc = folder_loc + "todo.txt"
    list_of_lines = []
    with open(file_loc) as f:
        for line in f:
            #line = f.readline()
            list_of_lines.append(line)
    return list_of_lines

def print_todos(todos):
    """
    Prints all todos in a list
    Args:
        todos: list[str]
    """
    for todo in todos:
        print(todo, end="")
    return


if __name__ == "__main__":
    action = get_action(sys.argv)
    if action == "help":
        print_help()
    elif action == "ls" or action == "list":
        todos = get_list_of_lines_in_file(folder)
        print_todos(todos=todos)
    else:
        print(action)

