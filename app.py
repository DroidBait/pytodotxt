import os
import sys
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

folder = config.get("General", "file_loc")

def print_help():
    print("Python Todo.txt Help")
    print("args:")
    print("    ls or list: List all todos in todo.txt file")
    print("        Example: app.py ls")
    print("        Filters can also be applied. Add a space between each filter")
    print("        Example: app.py ls @house +projectA")
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

def are_filters_applied(args):
    if len(args) > 2:
        return True
    else:
        return False

def filter_todos(args, todos):
    filter_keys = args[2:]
    filtered_todos = []
    for filter in filter_keys:
        for todo in todos:
            if filter in todo:
                if todo not in filtered_todos:
                    filtered_todos.append(todo)
    return filtered_todos


if __name__ == "__main__":
    action = get_action(sys.argv)
    if action == "help":
        print_help()
    elif action == "ls" or action == "list":
        todos = get_list_of_lines_in_file(folder)
        if are_filters_applied(sys.argv):
            filtered_todos = filter_todos(args=sys.argv, todos=todos)
            print_todos(filtered_todos)
        else:
            print_todos(todos=todos)
    else:
        print(action)

