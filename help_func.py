import glob
import json
import os
import sys
import time

from colorama import Fore
from numba import njit

import global_variables

FILE_NAME_WIDTH = 48
SIZE_WIDTH = 18
MODIFIED_WIDTH = 16
CREATED_WIDTH = 16


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
    print("find -")
    print("set search - set if the program should search in folders \n\t0 - no search, 1 - search in folders that matches filter, 2 - search all folders\n\t[set search 0/1/2]\n")
    print("set duplicity - set if the program should show duplicity \n\t[set duplicity 0/1]\n")
    print("show - show added files\n")
    print("save - save added files to variable\n\t[save to a]\n")
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

def read_added_folders():
    added_folders = []
    
    with open("added_folders.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            added_folders.append(line.strip())
        
    return added_folders

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

def search_folder(folder, commands=None, only_files=None):
    if commands == None:
        # files = glob.glob(folder + "\\*", recursive=True)
        # only_files = [d for d in files if os.path.isfile(d)]
        only_files = [f for f in glob(os.path.join(folder, '*')) if os.path.isfile(f)]
            
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
                files.extend(search_folder(folder, commands))
        elif global_variables.search_folders == 2:
            # all_directories = [os.path.abspath(entry.path) for entry in os.scandir(folder) if entry.is_dir()]
            try:
                all_directories = [os.path.abspath(entry.path) for entry in os.scandir(folder) if entry.is_dir()]
            except PermissionError:
                print(f"Access denied to the directory: {folder}")
                all_directories = []
            
            # all_directories = []
            # try:
            #     with os.scandir(global_variables.path) as entries:
            #         for entry in entries:
            #             if entry.is_dir():
            #                 all_directories.append(os.path.abspath(entry.path))
            # except PermissionError:
            #     print(f"Access denied to the directory: {global_variables.path}")
            # except Exception as e:
            #     print(f"An error occurred: {e}")
            
            for folder in all_directories:
                files.extend(search_folder(folder, commands, only_files=True))
                
        f = []
        
        if only_files == True:
            # f = [x for x in files if os.path.isfile(x)]
            # remove every directory from files
            for x in only_directories:
                files.remove(x)
            return files
        else:         
            for x in only_directories:
                files.remove(x)
            return files

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
    print(Fore.YELLOW + f"{len(files)} FILES:" + Fore.RESET)      # Number of occurances
    for file in files:
        file_name = file.split("\\")[-1]
        file_size = os.path.getsize(file)
        is_folder = os.path.isdir(file)
        if is_folder:
            print(f"{file_name:{FILE_NAME_WIDTH+SIZE_WIDTH+1}} {time_from_now(file, 'modified'):{MODIFIED_WIDTH}} {time_from_now(file, 'created'):{CREATED_WIDTH}}")  
        else:
            print(f"{file_name:{FILE_NAME_WIDTH}} {recalculate_size(file_size):{SIZE_WIDTH}} {time_from_now(file, 'modified'):{MODIFIED_WIDTH}} {time_from_now(file, 'created'):{CREATED_WIDTH}}")
            
def show_added_files(added_files):
    print("Added files:")
    for x in added_files:
        print(x)
            
def progress_bar(current, total, barLength = 20):
    progress = float(current) * 100 / total
    arrow = '=' * int(progress / 100 * barLength - 1) + '>'
    spaces = ' ' * (barLength - len(arrow))
    sys.stdout.write('\rProgress: [%s%s] %d%%' % (arrow, spaces, progress))
    sys.stdout.flush()
    
history = []

def add_history(command, files):
    history.append([command, files])
    
def print_history():
    print(Fore.YELLOW + f"History:" + Fore.RESET)
    for i, command in enumerate(history):
        print(f"[{i}] \"{command[0]}\"  \t  {len(command[1])} files")
        
def load_history(x : int):
    return history[x][1]