import glob
import json
import os
import time

from colorama import Fore

import global_variables


def help():
    print(Fore.YELLOW)
    print("Commands:")
    print("filter - filter a files based on specification \n\t[filter name output.txt] or [filter name output.txt size < 100] or [filter modified < 10 days]\n")
    print("add - add a files from filtered list \n\t[add file.txt] or [add *]\n")
    print("remove - remove a file from the list of files to be processed [remove file.txt]\n")
    print("set search - set if the program should search in folders \n\t[set search 0/1/2]\n0 - no search, 1 - search in folders that matches filter, 2 - search all folders\n")
    print("set duplicity - set if the program should show duplicity \n\t[set duplicity 0/1]\n")
    print("exit - exit the program\n")
    
    print("\nTo set default size unit type 'set unit [unit]'")
    print("0 - bytes")
    print("1 - kilobytes")
    print("2 - megabytes")
    print("3 - gigabytes")
    print(Fore.RESET)  
    
def read_json(file):    
    with open(file) as json_file:
        data = json.load(json_file)
        
    # TODO: Maybe write beter
    global_variables.default_unit = data["unit"]
    
    global_variables.search_folders = data["search_folders"]
        
    global_variables.show_duplicity = data["show_duplicity"]

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

def search_folder(folder, commands=None):
    if commands == None:
        files = glob.glob(folder + "\\*", recursive=True)
        only_files = [d for d in files if os.path.isfile(d)]
            
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
            
        files_from_folders = []
        
        if global_variables.search_folders == 1:
            for folder in only_directories:
                files_from_folders.extend(search_folder(folder, commands))
        elif global_variables.search_folders == 2:
            all_files = glob.glob(folder + "\\*", recursive=True)
            all_directories = [d for d in all_files if os.path.isdir(d)]
            for folder in all_directories:
                files_from_folders.extend(search_folder(folder, commands))
                
        f = files.copy()
        
        for x in files_from_folders:
            if os.path.isfile(x):
                f.append(x)
                    
        return f

def process_command(command : str) -> list:
    parts = []

    split_command = command.split()

    i = 0
    while i < len(split_command):
        if split_command[i].startswith('"'):
            quoted_part = split_command[i]
            while not split_command[i].endswith('"'):
                i += 1
                quoted_part += ' ' + split_command[i]
            parts.append(quoted_part)
        else:
            parts.append(split_command[i])
        i += 1

    return parts

def show_files(files):
    print(Fore.GREEN + f"Found {len(files)} files:" + Fore.RESET)      # Number of occurances
    for file in files:
        file_name = file.split("\\")[-1]
        file_size = os.path.getsize(file)
        is_folder = os.path.isdir(file)
        if is_folder:
            print(f"{file_name:48}")
        else:
            print(f"{file_name:35} {recalculate_size(file_size):13}")