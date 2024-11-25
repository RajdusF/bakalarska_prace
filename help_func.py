import glob
import json
import os
import sys
import time

from colorama import Fore

import global_variables
from command_functions import (add, add_folder, input_files, output, remove,
                               save, select, set_operations, settings,
                               show_files, sort)


def help():
    print(Fore.YELLOW)
    print("Arguments:", end=" ")
    print(Fore.RESET)
    print("-p - path to the folder [py main.py -p \"C:\\Users\\Filip\\Documents\\bakalarska_prace\\files]")
    print("-c - command to process immediately after start [py main.py -c \"filter name *.txt\"]")
    print(Fore.YELLOW)
    print("Commands:", end=" ")
    print(Fore.RESET)
    print("* - show all files in the folder\n")
    print("cd - show actual directory\n")
    print("cd .. - go to parent directory\n")
    print("cd [folder] - go to folder\n")
    print("filter - filter a files based on specification \n\t[filter name output.txt]\n\t[filter name output.txt size < 100]\n\t[filter modified < 10 days]\n\t[filter name *.txt created < 30 days]\n")
    print("add - add a files from filtered list \n\t[add file.txt] or [add *]\n")
    print("remove - remove a file from the list of files to be processed\n\t[remove file.txt]\n\t[remove *]\n")
    print("sort - sort files based on specification \n\t[sort by name] or [sort by name desc]\n\t[sort by size] or [sort by size desc]\n\t[sort by modified] or [sort by modified desc]\n\t[sort by created] or [sort by created desc]\n")
    print("select - select top or bottom files \n\t[select top 10] or [select bottom 10]\n")
    print("find -\n")
    print("set search - set if the program should search in folders \n\t0 - no search, 1 - search in folders that matches filter, 2 - search all folders\n\t[set search 0/1/2]\n")
    print("set duplicity - set if the program should show duplicity \n\t[set duplicity 0/1]\n")
    print("show - show added files\n")
    print("save - save (files/added files) to variable\n\t[save files/added to a]\n")
    print("load - load added files from variable\n\t[load from a]\n")
    
    print("set unit - set default size unit type\n\t[set unit 0/1/2/3]")
    print("\t0 - bytes")
    print("\t1 - kilobytes")
    print("\t2 - megabytes")
    print("\t3 - gigabytes")
    
    print("\nexit - exit the program\n")
    
def read_json(file):    
    with open(file) as json_file:
        data = json.load(json_file)
        
    # TODO: Maybe write beter
    global_variables.default_unit = data["unit"]
    
    global_variables.search_folders = data["search_folders"]
        
    global_variables.show_duplicity = data["show_duplicity"]
    
    global_variables.path = data["path"]


def recalculate_size(size: int) -> int:
    unit = global_variables.default_unit
    
    if unit == "GB":
        if size > 1024 * 1024 * 1024:
            return "{:11,.2f} GB".format(size / 1024 / 1024 / 1024).replace(',', ' ')
        elif size > 1024 * 1024:
            return "{:11,.2f} MB".format(size / 1024 / 1024).replace(',', ' ')
        elif size > 1024:
            return "{:11,.2f} KB".format(size / 1024).replace(',', ' ')
        else:
            return "{:11,.2f} B".format(size).replace(',', ' ')
        
    elif unit == "MB":
        if size > 1024 * 1024:
            return "{:11,.2f} MB".format(size / 1024 / 1024).replace(',', ' ')
        elif size > 1024:
            return "{:11,.2f} KB".format(size / 1024).replace(',', ' ')
        else:
            return "{:11,.2f} B".format(size).replace(',', ' ')
        
    elif unit == "KB":
        if size > 1024:
            return "{:11,.2f} KB".format(size / 1024).replace(',', ' ')
        else:
            return "{:11,.2f} B".format(size).replace(',', ' ')
        
    else:
        return "{:11,.2f} B".format(size).replace(',', ' ')

def time_from_now(file : str, option : str) -> str:
    # TODO: Maybe place time before this function begins
    current_time = time.time()
    if option == "modified":
        modification_time = os.path.getmtime(os.path.join(file))
        seconds_from_now = current_time - modification_time
    elif option == "created":
        created_time = os.path.getctime(os.path.join(file))
        seconds_from_now = current_time - created_time

    if seconds_from_now < 60:
        return f"{seconds_from_now:8.2f} s"
    elif seconds_from_now < 3600:
        return f"{seconds_from_now / 60:8.2f} m"
    elif seconds_from_now < 86400:
        return f"{seconds_from_now / 3600:8.2f} h"
    elif seconds_from_now < 604800:
        return f"{seconds_from_now / 86400:8.2f} d"
    else:
        return f"{seconds_from_now / 604800:8.2f} w" 

def search_folder(folder, commands=None, only_files=None, progress=None, progress_total=None):
    num_of_folders = 0
    
    if commands == None:
        only_files = []
        for f in glob.glob(os.path.join(folder, '*')):
            if os.path.isfile(f):
                only_files.append(f)
            else:
                num_of_folders += 1
            
        return only_files
    else:
        name = None
        
        if "name" in commands:
            name_index = commands.index("name") + 1
            if name_index < len(commands):
                name = commands[name_index]    
        elif commands[commands.index("filter") + 1] == "*":
            name = "*" 
                
                
        if name:
            if "name" in commands and commands[commands.index("name") - 1] == "not":                # NOT NAME
                all_files = glob.glob(folder + "\\*", recursive=True)
                name_files = glob.glob(folder + "\\" + name, recursive=True)
                files = [file for file in all_files if file not in name_files]
                
                only_directories = [d for d in files if os.path.isdir(d)]
            else:                                                                                   # NAME
                files = glob.glob(folder + "\\" + name, recursive=True)
                only_directories = [d for d in files if os.path.isdir(d)]
        else:                                                                                       # NO NAME                      
            files = glob.glob(folder + "\\*", recursive=True)
            only_directories = [d for d in files if os.path.isdir(d)]
            
        if global_variables.search_folders == 1:
            for folder in only_directories:
                files.extend(search_folder(folder, commands))
        elif global_variables.search_folders == 2:
            try:
                all_directories = [os.path.abspath(entry.path) for entry in os.scandir(folder) if entry.is_dir()]
            except PermissionError:
                print(f"\rAccess denied to the directory: {folder}")
                progress_bar(progress, progress_total, 30)
                # sys.stdout.flush()
                all_directories = []
            
            for folder in all_directories:
                temp_files, num_of_folders = search_folder(folder, commands, only_files=True, progress=progress, progress_total=progress_total)
                files.extend(temp_files)
                
        f = []
        
        num_of_folders += len(only_directories)
        
        if only_files == True:
            for x in only_directories:
                files.remove(x)
            return files, num_of_folders
        else:         
            for x in only_directories:
                files.remove(x)
            return files, num_of_folders

# OLD TO PROCESS QUOTES
# def process_command(command : str) -> list:
#     parts = []

#     split_command = command.split()

#     i = 0
#     while i < len(split_command):
#         if split_command[i].startswith('"'):
#             quoted_part = split_command[i]
#             while not split_command[i].endswith('"'):
#                 i += 1
#                 quoted_part += ' ' + split_command[i]
#             parts.append(quoted_part)
#         else:
#             parts.append(split_command[i])
#         i += 1

#     return parts

def process_command(command : str, dict, files : list, added_files : list):
    from filter import filter
    
    commands = command.split(" ")
        
    if command == "exit":
        return -1
    
    if command == "?":
        help()
        return
    
    if "**" in command:
        print("Wrong input")
        return
    
    if command == "*":
        for file in os.listdir(global_variables.path):
            print(file)
            
    elif command == "cd.." or command == "cd ..":
        global_variables.path = os.path.abspath(os.path.join(global_variables.path, os.pardir))
        print(Fore.GREEN + f"Current path: {global_variables.path}" + Fore.RESET)
        
    elif "cd" in command:
        path_index = commands.index("cd") + 1
        if path_index < len(commands):
            path = commands[path_index]
            if os.path.isdir(path):
                global_variables.path = path
                print(Fore.GREEN + f"Current path: {global_variables.path}" + Fore.RESET)
            elif os.path.isdir(global_variables.path + "\\" + path):
                global_variables.path = global_variables.path + "\\" + path
                print(Fore.GREEN + f"Current path: {global_variables.path}" + Fore.RESET)
            else:
                print("Path not found")
        else:
            print(Fore.GREEN + f"Current path: {global_variables.path}" + Fore.RESET)
            
    elif "filter" in commands:
        files.extend(filter(commands, files, added_files))
        add_history(command, files)
    
    elif "sort" in commands:
        temp = sort(commands, files)
        files.clear()
        files.extend(temp)
        add_history(command, files)
        
    elif "select" in commands:
        temp = select(commands, files)
        files.clear()
        files.extend(temp)
        add_history(command, files)
    
    elif "find" in commands:
        finds = []
        for file in added_files:
            finds.extend(find(commands[commands.index("find") + 1:], file))
            
        print(Fore.GREEN + f"Found {len(finds)} occurances:" + Fore.RESET)
        for find in finds:
            print(find)
    
    elif "add" in commands:
        if commands[1] == "*" and len(commands) == 2:
            add("*", files, added_files)
        elif "\\" in command and len(commands) == 2:
            added_files.extend(add_folder(commands[1]))
        elif "\\" in command and len(commands) == 3 and commands[1] == "all":
            added_files.extend(add_folder(commands[2], recursive=True))
            
        elif len(commands) == 2:
                name = commands[1]
                add(name, files, added_files)
        else:
            print("Wrong input")
            return
        
        print(f"Added files ({len(added_files)}):")
        for x in added_files:
            print(x)
            
    elif "remove" in commands:
        r = remove(commands, added_files)
        print(f"Removed {r} files")
            
    elif "show" in commands:
        if len(commands) == 2 and commands[1] == "added":
            show_added_files(added_files)
        elif len(commands) == 2 and commands[1] == "files":
            show_files(files)
        elif len(commands) == 2:                          # dict[commands[1]]):
            if dict.get(commands[1]) != None:
                print(f"Files in \"{commands[1]}\":")
                for x in dict[commands[1]]:
                    print(x)
            else:
                print(f"Save file {commands[4]} not found")
                return
        else:
            print("Added files:")
            for x in added_files:
                print(x)
        
    elif "set" in commands:
        if "unit" in commands and len(commands) == 3:
            settings(0, commands[2])
        elif "search" in commands and len(commands) == 3:
            settings(1, int(commands[2]))
        elif "duplicity" in commands or "duplicate" in commands and len(commands) == 3:
            settings(2, int(commands[2]))
        elif "path" in commands and len(commands) == 3:
            settings(3, commands[2])
        elif len(commands) == 1:
            print(f"Default unit: {global_variables.default_unit}")
            print(f"Search folders: {global_variables.search_folders}")
            print(f"Show duplicity: {global_variables.show_duplicity}")
            return

        
    elif commands[0] == "save" and commands[2] == "to" and len(commands) == 4:
        if commands[1] == "files":
            save(commands[3], files, dict)
        elif commands[1] == "added":
            save(commands[3], added_files, dict)
        else:
            print("Wrong input")
        
    elif commands[0] == "load" and commands[1] == "from" and command[3] == "to" and len(commands) == 5:
        if commands[2] in dict:
            if commands[4] == "files":
                files = dict[commands[2]].copy()
                print("Files loaded from \"" + commands[2] + "\"")
            else:
                added_files = dict[commands[2]].copy()
                print("Files loaded from \"" + commands[2] + "\"")
        else:
            print("File not found")
                
    elif "input" in commands:
        if len(commands) == 1:
            input_files(added_files)
        elif len(commands) == 2:
            input_files(added_files, commands[1])
    
    elif "output" in commands:
        extend_choice = True if "extend" in commands else False
             
        if len(commands) == 1:
            output(added_files, extend=extend_choice)
        elif len(commands) == 2:
            output(added_files, output_file=commands[1], extend=extend_choice)
        
    elif "history" in commands and len(commands) == 1:
        print_history()
        
    elif "history" in commands and len(commands) == 2:
        try:
            temp = load_history(int(commands[1]))
            files.clear()
            files.extend(temp)
            show_files(files)
        except:
            print("Wrong input")
            
    elif "ls" in commands and len(commands) == 1:
        show_current_folder()
        
    # Sjednocení, průnik, rozdíl
    elif "A" in commands or "U" in commands or "-" in commands:
        temp = set_operations(command, dict)
        files.clear()
        files.extend(temp)
        add_history(command, files)
        
        
    elif command == "":
        return
    
    else:
        print("Wrong input")
            
def show_added_files(added_files):
    print("Added files:")
    for x in added_files:
        print(x)
        
def show_current_folder():
    print(f"{"file":{global_variables.FILE_NAME_WIDTH+4}} {"size":{global_variables.SIZE_WIDTH}} {"modified":{global_variables.MODIFIED_WIDTH}} {"created":{global_variables.CREATED_WIDTH}}")
    for file in glob.glob(global_variables.path + "\\*", recursive=True):
        file_name = file.split("\\")[-1]
        is_folder = os.path.isdir(file)
        file_size = os.path.getsize(file)
        if is_folder:
            print(f"{file_name:{global_variables.FILE_NAME_WIDTH+global_variables.SIZE_WIDTH+1}} {time_from_now(file, 'modified'):{global_variables.MODIFIED_WIDTH}} {time_from_now(file, 'created'):{global_variables.CREATED_WIDTH}}")
        elif not is_folder:
                print(f"{file_name:{global_variables.FILE_NAME_WIDTH}} {recalculate_size(file_size):{global_variables.SIZE_WIDTH}} {time_from_now(file, 'modified'):{global_variables.MODIFIED_WIDTH}} {time_from_now(file, 'created'):{global_variables.CREATED_WIDTH}}")
            
def progress_bar(current, total, barLength = 20):
    progress = float(current) * 100 / total
    arrow = '=' * int(progress / 100 * barLength - 1) + '>'
    spaces = ' ' * (barLength - len(arrow))
    sys.stdout.write('\rProgress: [%s%s] %d%%' % (arrow, spaces, progress))
    sys.stdout.flush()
    
history = []

def add_history(command, input_files):
    files = input_files.copy()
    history.append([command, files])
    
def print_history():
    print(Fore.YELLOW + f"History:" + Fore.RESET)
    for i, command in enumerate(history):
        print(f"[{i}] \"{command[0]}\"  \t  {len(command[1])} files")
        
def load_history(x : int):
    return history[x][1]
    
def read_commands_from_file():
    try:
        with open("commands.txt", "r") as file:
            commands = [line.strip() for line in file.readlines()]
        
        return commands

    except FileNotFoundError:
        print(Fore.RED + "The file 'commands.txt' does not exist" + Fore.RESET)
        return None