import json
import os

import global_variables
from help_func import search_folder, show_files


def add(name : str, files : list, added_files : list):
    i = len(added_files)
    for x in files:
        if name in x:
            name = x
            break
        
    # if is folder
    if os.path.isdir(name):
        added_files.extend(search_folder(name))
    else:
        if name == "*":
            for x in files:
                if x not in added_files:
                    added_files.append(x)
        elif name in files:
            if name not in added_files:
                added_files.append(name)
            else:
                print("File already added")
        else:
            print("File not found")
            return 0
        
    print(f"Added {len(added_files) - i} files")
    return(len(added_files) - i)


def settings(option, value):
    unit = None
    search_folders = None
    show_duplicity = None
    
    if option == 0:
        if value == "0":
            print("Size unit set to bytes")
            unit = "B"
        elif value == "1":
            print("Size unit set to kilobytes")
            unit = "KB"
        elif value == "2":
            print("Size unit set to megabytes")
            unit = "MB"
        elif value == "3":
            print("Size unit set to gigabytes")
            unit = "GB"
        else:
            print("Wrong input")
    elif option == 1:
        if value == 0:
            print("Search folders set to \"Do not search folders\"")
        elif value == 1:
            print("Search folders set to \"Search folders that matches filter\"")
        elif value == 2:
            print("Search folders set to \"Search all folders\"")
        else:
            print("Wrong input")
            return
        search_folders = value
            
    elif option == 2:
        if value == 1:
            print("Show duplicity set to True")
            show_duplicity = True
        elif value == 0:
            print("Show duplicity set to False")
            show_duplicity = False
    else:
        print("Wrong input")
    
    settings_data = {}

    settings_path = os.path.join(os.path.dirname(__file__), 'settings.json')
    
    if unit is not None:
        settings_data["unit"] = unit
        global_variables.default_unit = unit
    else:
        settings_data["unit"] = global_variables.default_unit

    if search_folders is not None:
        settings_data["search_folders"] = search_folders
        global_variables.search_folders = search_folders
    else:
        settings_data["search_folders"] = global_variables.search_folders
        
    if show_duplicity is not None:
        settings_data["show_duplicity"] = show_duplicity
        global_variables.show_duplicity = show_duplicity
    else:
        settings_data["show_duplicity"] = global_variables.show_duplicity

    with open(settings_path, 'w') as json_file:
        json.dump(settings_data, json_file, indent=4)


def find(commands, input_file : str):       
    sentence = None
    variable = None
    operator = None
    comparing_size = None
    collumn_index = -1
    collumns = []
    lines_to_return = []
    
    for command in commands:
        if command.startswith('"') and command.endswith('"'):
            sentence = command[1:-1]
    
    if len(commands) == 3 and "<" in commands or ">" in commands or "=" in commands:
        variable = commands[0]
        operator = commands[1]
        comparing_size = int(commands[2])
    
    with open(input_file) as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if len(commands) == 1 or type(commands) == str:
                if (commands[0] in line and type(commands) == list) or (type(commands) == str and commands in line):
                    return line
                
            elif commands[0] == "all" and sentence in line:
                lines_to_return.append(line)
            
            
            elif sentence and sentence in line:
                return line
            
            
            elif len(commands) == 2 and commands[0] == "all" and commands[1] in line:
                lines_to_return.append(line)
                
            elif variable and operator and comparing_size:
                words = line.split()
                if len(collumns) == 0:
                    if words[0] == "#h":
                        collumns = words[1:]
                        collumn_index = collumns.index(variable)
                
                else:
                    if collumn_index != -1 and words[0] != "#f":
                        number = words[collumn_index]
                        if eval(f"{number} {operator} {comparing_size}"):
                            return line
                        
    return lines_to_return

def sort(commands, files):
    if commands[1] == "desc" and len(commands) == 2:
        r = sorted(files, reverse=True)
        show_files(r)
        return r
    elif commands[1] == "by" and commands[2] == "size":
        if len(commands) == 3:
            r = sorted(files, key=os.path.getsize, reverse=True)
            show_files(r)
            return r
        elif commands[3] == "desc":
            r = sorted(files, key=os.path.getsize)
            show_files(r)
            return r
    elif commands[1] == "by" and commands[2] == "modified":
        if len(commands) == 3:
            r = sorted(files, key=os.path.getmtime, reverse=True)
            show_files(r)
            return r
        elif commands[3] == "desc":
            r = sorted(files, key=os.path.getmtime)
            show_files(r)
            return r
        
def select(commands, files):
    if commands[1] == "top":
        if len(commands) == 3:
            r = files[:int(commands[2])]
            show_files(r)
            return r
    elif commands[1] == "bottom":
            r = files[-int(commands[2]):]
            show_files(r)
            return r
    return 

def output(added_files):
    with open('output.txt', 'w') as f:
        for file in added_files:
            if os.path.isfile(file):
                f.write(file + '\n')
            
    print("Added files saved to output.txt")