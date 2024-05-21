import sys
import configparser
import re
import datetime

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
    print("    add: Add a new todo")
    print("        Example: app.py add")
    print("    done: Complete a task")
    print("        Example: app.py done 2")
    print("    del or delete: Removes completed tasks from file")
    print("        Example: app.py del")
    print("    schedule or sched: List tasks due today, then list overdue tasks")
    print("        Example: app.py sched")
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
    current_line_num = 0
    with open(file_loc) as f:
        for line in f:
            current_line_num = current_line_num + 1
            list_of_lines.append(str(current_line_num) + " " + line)
    return list_of_lines

def addToFile(folder_loc, text):
    textFile = folder_loc + "todo.txt"
    with open(textFile, "a") as f:
        f.write(text)

def removeCompletedTodos(todos):
    non_completed_todos = []
    for todo in todos:
        if todo[2] != "x":
            non_completed_todos.append(todo)
    return non_completed_todos

def print_todos(todos):
    """
    Prints all todos in a list. 
    Starts by filtering out all completed todos
    Prints the rest
    Args:
        todos: list[str]
    """
    todo_list = removeCompletedTodos(todos=todos)
    for todo in todo_list:
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

def isPriorityValid(input):
    if len(input) == 0:
        return ""
    if isinstance(input, str):
        if len(input) == 1:
            pattern = re.compile(r"[A-Za-z]")
            if pattern.match(input):
                return "(" + input.upper() + ") "
            else:
                print("Priority must be a single letter A-Z")
                sys.exit()
        else:
            print("Priority must be a single letter A-Z")
            sys.exit()
    else:
        print("Priority must be a single letter A-Z")
        sys.exit()

def splitUpStrToList(text, prefix):
    items = text.split(",")
    outputStr = ""
    for item in items:
        if item[0] == prefix:
            outputStr = outputStr + item + " "
        else:
            outputStr = outputStr + prefix + item + " "
    return outputStr

def setupProjects(projectText):
    if len(projectText) == 0:
        return ""
    if "," in projectText:
        projectsList = splitUpStrToList(projectText, "@")
        return projectsList
    else:
        if projectText[0] == "@":
            return projectText.replace(" ", "") + " "
        else:
            return "@" + projectText.replace(" ", "") + " "

def setupContexts(contextText):
    if len(contextText) == 0:
        return ""
    if "," in contextText:
        contextsList = splitUpStrToList(contextText, "+")
        return contextsList
    else:
        if contextText[0] == "+":
            return contextText.replace(" ", "") + " "
        else:
            return "+" + contextText.replace(" ", "") + " "

def validateDueDate(date):
    if len(date) == 0:
        return ""
    pattern = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", re.IGNORECASE)
    if pattern.match(date):
        return "due:" + date
    else:
        print("Date must match the pattern YYYY-MM-DD")
        sys.exit()

def validateTaskText(taskText):
    if len(taskText) == 0:
        print("You must enter a task description")
        sys.exit()
    else:
        return taskText + " "

def addNewTodo():
    print("Enter a new todo: leave input blank if not needed")
    priority = input("Enter Priority (A - Z): ")
    validPriority = isPriorityValid(priority)

    task = input("Enter task description: ")
    validTask = validateTaskText(task)

    print("If entering multiple projects or contexts put a , between each. Not needed for singular item")
    projects = input("Enter project(s): ")
    validatedProjs = setupProjects(projects)

    contexts = input("Enter context(s): ")
    validatedContexts = setupContexts(contexts)

    due_date = input("Enter due date YYYY-MM-DD: ")
    validDate = validateDueDate(due_date)

    textToAdd = validPriority + validTask + validatedProjs + validatedContexts + validDate + "\n"
    addToFile(folder, textToAdd)
    print("Text: " + textToAdd + "Added to file")
    sys.exit()

def getTaskFromNumber(folder_loc, num):
    file_loc = folder_loc + "todo.txt"
    current_line_num = 0
    with open(file_loc) as f:
        for line in f:
            current_line_num = current_line_num + 1
            if current_line_num == int(num):
                return line
    print("Task not found")
    sys.exit()

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

def removeCompletedTasks(folder_loc):
    file_loc = folder_loc + "todo.txt"
    with open(file_loc, 'r') as file:
        lines = file.readlines()

    # delete matching content
    content = "This line doesn't belong"
    with open(file_loc, 'w') as file:
        for line in lines:
            # readlines() includes a newline character
            if line[0] != "x":
                file.write(line)

def scheduledTasks(todos):
    todaysDate = datetime.datetime.now()
    dueToday = []
    overdue = []

    for todo in todos:
        if 'due:' in todo:
            linesplit = todo.split("due:")[1]
            dateOfTask = linesplit[0:10]
            dateObj = datetime.datetime.strptime(dateOfTask, "%Y-%m-%d")
            if dateObj.date() < todaysDate.date():
                overdue.append(todo)
            if dateObj.date() == todaysDate.date():
                dueToday.append(todo)
    
    return dueToday, overdue

def printScheduledTasks(dueToday, overdue):
    if len(dueToday) == 0 and len(overdue) == 0:
        print("There are no tasks due today or overdue")
    if len(dueToday) > 0:
        print("Todays Tasks:")
        print_todos(dueToday)
        print(" ")
    if len(overdue) > 0:
        print("Overdue Tasks:")
        print_todos(overdue)

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
    elif action == "add":
        addNewTodo()
    elif action == "done":
        if len(sys.argv) > 2:
            numberSelected = sys.argv[2]
            taskToComplete = getTaskFromNumber(folder, numberSelected)
            if taskToComplete[0] == "x":
                print("Task has already been marked as complete")
            else:
                replace_line(folder + "todo.txt", int(sys.argv[2]) - 1, "x " + taskToComplete)
                print("Task {} marked as complete".format(sys.argv[2]))
        else:
            print("Make sure you are providing a number after the done flag")
    elif action == "del" or action == "delete":
        removeCompletedTasks(folder)
        print("All completed tasks have been deleted from the todo.txt file")
    elif action == "schedule" or action == "sched":
        todos = get_list_of_lines_in_file(folder)
        dueToday, overdue = scheduledTasks(todos)
        printScheduledTasks(dueToday, overdue)
    else:
        print("Action not recognised")
        print_help()
