# pytodotxt
A python script to copy the features of todo.txt

## Initial setup
1. Copy the example-config.ini and created a version called config.ini `cp example-config.ini config.ini`
2. Edit the folder_loc in the config.ini file to where you want to store your todo.txt file
3. In the folder location listed in the config.ini file, create a file called todo.txt
4. run `python3 app.py ls` to show an empty list or `python3 app.py add` to add your first task

Note: This currently does not support archiving completed tasks into a done.txt file. Instead, you can delete all completed tasks from the file

Supported operations:
list / ls (supports filtering based on input text)
add
done
delete / del
schedule / sched
