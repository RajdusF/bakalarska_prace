import glob
import json
import os
import sys
import time

from colorama import Fore

import python.global_variables as global_variables

history = []

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
                # TODO: try changing "only_files"
                # files.extend(search_folder(folder, commands))
                
                temp_files, num_of_folders_returned = search_folder(folder, commands)
                num_of_folders += num_of_folders_returned
                files.extend(temp_files)
        elif global_variables.search_folders == 2:
            try:
                all_directories = [os.path.abspath(entry.path) for entry in os.scandir(folder) if entry.is_dir()]
            except PermissionError:
                print(f"\rAccess denied to the directory: {folder}")
                progress_bar(progress, progress_total, 30)
                # sys.stdout.flush()
                all_directories = []
            
            for folder in all_directories:
                temp_files, num_of_folders_returned = search_folder(folder, commands, only_files=True, progress=progress, progress_total=progress_total)
                num_of_folders += num_of_folders_returned
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
    if total == 0:
        return
    progress = float(current) * 100 / total
    arrow = '=' * int(progress / 100 * barLength - 1) + '>'
    spaces = ' ' * (barLength - len(arrow))
    sys.stdout.write('\rProgress: [%s%s] %d%%' % (arrow, spaces, progress))
    sys.stdout.flush()

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
        with open("configurator_commands.txt", "r") as file:
            commands = [line.strip() for line in file.readlines()]
        
        return commands

    except FileNotFoundError:
        print(Fore.RED + "The file 'configurator_commands.txt' does not exist" + Fore.RESET)
        return None
    
def my_help():
    print(Fore.YELLOW)
    print("Arguments:", end=" ")
    print(Fore.RESET)
    print("-p - path to the folder [py main.py -p \"C:\\Users\\Filip\\Documents\\bakalarska_prace\\files]")
    print(Fore.YELLOW)
    print("Commands:", end=" ")
    print(Fore.RESET)
    print("* - show all files in the folder\n")
    help_cd()
    
    help_filter()
    help_add()
    help_remove()
    help_sort()
    
    print("find -\n")
    print("set search - set if the program should search in folders \n\t0 - no search, 1 - search in folders that matches filter, 2 - search all folders\n\t[set search 0/1/2]\n")
    print("set duplicity - set if the program should show duplicity \n\t[set duplicity 0/1]\n")
    print("show - show added files\n")
    print("save - save (files/added files) to variable\n\t[save files/added to a]\n")
    print("load - load added files from variable\n\t[load from a]\n")
    
    help_output()
    
    print("set unit - set default size unit type\n\t[set unit 0/1/2/3]")
    print("\t0 - bytes")
    print("\t1 - kilobytes")
    print("\t2 - megabytes")
    print("\t3 - gigabytes")
    
    print("\nexit - exit the program\n")
    
def help_cd():
    print("cd - show actual directory")
    print("\tcd .. - go to parent directory")
    print("\tcd [folder] - go to folder")
    print("\t[folder] can be relative as \"Documents\" same as absolute \"C:\\Users\\Documents\"\n")
    
def help_filter():
    print("filter - filter a files based on specification \n\t[filter name output.txt]\n\t[filter name output.txt size < 100]\n\t[filter modified < 10 days]\n\t[filter name *.txt created < 30 days]")
    print("\t[filter files size > 1000 KB]\n\t[filter added_files name *.txt]\n")
    
def help_add():
    print("add - add a files from filtered list \n\t[add file.txt] or [add *]\n\t[add C:\\Users\\Documents] - to add whole folder\n")
    print("\t[add all C:\\Users\\Documents] - to add whole folder recursively with files in subfolders\n")
    
def help_remove():
    print("remove - remove a file from the list of files to be processed\n\t[remove file.txt]\n\t[remove *]\n")
    
def help_sort():
    print("sort - sort files based on specification \n\t[sort by name] or [sort by name desc]\n\t[sort by size] or [sort by size desc]\n\t[sort by modified] or [sort by modified desc]\n\t[sort by created] or [sort by created desc]\n")
    
def help_select():
    print("select - select top or bottom files \n\t[select top 10] or [select bottom 10]\n")
    
def help_output():
    print("output - output files to the console\n\t[output] or [output file.txt] or [output file.txt extend] - to extend the output file\n")