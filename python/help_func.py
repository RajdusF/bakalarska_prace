import glob
import json
import os
import sys
import time

from colorama import Fore, Style, init
from tabulate import tabulate

import python.global_variables as global_variables

history = []


def get_variable(message : str, find_occurances : list):
    r = []
    
    # occurances
    if message.startswith("occurances") and "[" not in message and "]" not in message:
        for i, x in enumerate(find_occurances):
            r.append(x)
            
        print_occurances(find_occurances)
        return r
    
    # occurances[0]
    # elif "occurances" in message and "[" in message and "]" in message and message.count("[") == 2 and message.count("]") == 2:
    #     try:
    #         index = int(message[message.index("[") + 1:message.index("]")])
    #         second_bracket_index = int(message.find("[", message.index("[") + 1))
    #         part = int(message[second_bracket_index + 1: message.index("]", second_bracket_index)])
    #         for occurance in find_occurances:
    #             # print(occurance[index])
    #             r.append(occurance[index].split("\\")[-2])
    #         return r
    #     except:
    #         pass
    
    # occurances[0][0]
    elif message.startswith("occurances") and "[" in message and "]" in message:
        try:
            index = int(message[message.index("[") + 1:message.index("]")])
            for occurance in find_occurances:
                # print(occurance[index])
                r.append(occurance[index])
            return r
        except:
            pass
    
    # occurance
    elif message.startswith("occurance") and "[" in message and "]" in message:
        try:
            index = int(message[message.index("[") + 1:message.index("]")])
            # print(f"{index}: {find_occurances[index]}")
            return find_occurances[index]
        except:
            pass
    
    raise Exception("Variable not found")


def take_int(message : str, position : int = 0):
    try:      
        numbers = []
        current_number = ""

        for char in message:
            if char.isdigit():
                current_number += char
            elif current_number:
                numbers.append(int(current_number))
                current_number = ""

        if current_number:
            numbers.append(int(current_number))
            
        if position >= len(numbers):
            print("Number not found")
            return
            
        print(f"Number {position}: {numbers[position]}")
        return numbers[position]
    except:
        return None
    
def take_float(message : str, position : int = 0):
    try:
        numbers = []
        current_number = ""
        decimal = False

        for char in message:
            if char.isdigit():
                current_number += char
            elif char == "." and not decimal:
                current_number += char
                decimal = True
            elif current_number:
                numbers.append(float(current_number))
                current_number = ""
                decimal = False

        if current_number:
            numbers.append(float(current_number))
            
        if position >= len(numbers):
            print("Number not found")
            return
            
        print(f"Number {position}: {numbers[position]}")
        return numbers[position]
    except:
        return None

def print_occurances(files):
    print(Fore.GREEN + f"Found {len(files)} occurances:" + Fore.RESET)
                    
    temp_occurences = []
    for i, occurance in enumerate(files):
        name, line = None, None
        if len(occurance[0]) > 40:
            name = "..." + occurance[0][-40:]
        else:
            name = occurance[0]
        if len(occurance[1]) > 60:
            line = occurance[1][-60:]
        else:
            line = occurance[1]
            
        temp_occurences.append([i, name, line])
    headers = ["Index", "File path", "Line"]

    table = tabulate(temp_occurences, headers=headers, tablefmt="grid")
    print(table)

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

def add_history(command, input_files, find_occurances=None):
    files = input_files.copy()
    
    if find_occurances:
        history.append([command, files, find_occurances.copy()])
    else:
        history.append([command, files, []])
    
def print_history():
    print(Fore.YELLOW + "History:" + Fore.RESET)
    table = [[i, command[0], len(command[1]), len(command[2])] for i, command in enumerate(history)]
    print(tabulate(table, headers=["Index", "Command", "File Count", "Finds"], tablefmt="pretty", colalign=("center", "left", "center", "center")))
        
def load_history(x : int, files : list, find_occurances : list):
    try:
        files.clear()
        files.extend(history[x][1])
        find_occurances.clear()
        find_occurances.extend(history[x][2])
    except IndexError:
        print(Fore.RED + "Index out of range" + Fore.RESET)
        return -1
    except Exception as e:
        print(Fore.RED + f"Error: {e}" + Fore.RESET)
        return -1
    
    return 0
    
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
    print("-p - path to the folder [py configurator.py -p \"C:\\Users\\Filip\\Documents\\bakalarska_prace\\files]")
    print(Fore.YELLOW)
    print("Commands:", end=" ")
    print(Fore.RESET)
    
    
    print(Fore.LIGHTCYAN_EX + "*" + Fore.RESET + " - show all files in the current folder\n")

    help_cd()
    help_filter()
    help_add()
    help_remove()
    help_sort()
    help_select()
    
    help_find()
    help_take_int()
    help_take_float()
    
    help_show()
    help_save()
    help_load()
    help_output()
    help_input()
    help_names()
    help_set_search()
    help_set_duplicity()
    help_set_unit()
    
    help_history()
    
    print(Fore.LIGHTCYAN_EX + "\nexit" + Fore.RESET +" - exit the program\n")
    
def help_cd():
    print(Fore.LIGHTCYAN_EX + "cd" + Fore.RESET + " - show actual directory")
    print("\tcd .. - go to parent directory")
    print("\tcd [folder] - go to folder")
    print("\t[folder] can be relative as \"Documents\" same as absolute \"C:\\Users\\Documents\"\n")
    
def help_filter():
    print(Fore.LIGHTCYAN_EX + "filter" + Fore.RESET + " - filter files based on specification")
    print("\t[filter name output.txt]")
    print("\t[filter name output.txt size < 100]")
    print("\t[filter modified < 10 days]")
    print("\t[filter name *.txt created < 30 days]")
    print("\t[filter files size > 1000 KB]")
    print("\t[filter added_files name *.txt]\n")
    
def help_add():
    print(Fore.LIGHTCYAN_EX + "add" + Fore.RESET + " - add files from filtered list")
    print("\t[add file.txt] or [add *]")
    print("\t[add C:\\Users\\Documents] - to add whole folder")
    print("\t[add all C:\\Users\\Documents] - to add whole folder recursively with files in subfolders\n")
    
def help_remove():
    print(Fore.LIGHTCYAN_EX + "remove" + Fore.RESET + " - remove a file from the list of files to be processed")
    print("\t[remove file.txt]")
    print("\t[remove *]\n")
    
def help_sort():
    print(Fore.LIGHTCYAN_EX + "sort" + Fore.RESET + " - sort files based on specification")
    print("\t[sort by name] or [sort by name desc]")
    print("\t[sort by size] or [sort by size desc]")
    print("\t[sort by modified] or [sort by modified desc]")
    print("\t[sort by created] or [sort by created desc]\n")
    
def help_select():
    print(Fore.LIGHTCYAN_EX + "select" + Fore.RESET + " - select top or bottom files")
    print("\t[select top 10] or [select bottom 10]\n")
    
def help_find():
    print(Fore.LIGHTCYAN_EX + "find" + Fore.RESET + " - find string in files/added_files")
    print("\t[find \"string\" in files] or [find \"RESULT=1\" in added] or [find \"RESULT=1\"] finding in files if not specified\n")
    
def help_take_int():
    print(Fore.LIGHTCYAN_EX + "take_int" + Fore.RESET + " - take integer from the message (made for occurances after command \"find\")")
    print("\t[take_int(lines, 0) > 6000] - browsing in column with text or [take_int(file, 0)] - browsing in column with file path/file name\n")

def help_take_float():
    print(Fore.LIGHTCYAN_EX + "take_float" + Fore.RESET + " - take float from the message (made for occurances after command \"find\")")
    print("\t[take_float(lines, 0) > 6000,50] - browsing in column with text or [take_float(file, 0)] - browsing in column with file path/file name\n")
      
def help_output():
    print(Fore.LIGHTCYAN_EX + "output" + Fore.RESET + " - output files to the console")
    print("\t[output] or [output file.txt] or [output file.txt extend] - to extend the output file\n")
    
def help_set_search():
    print(Fore.LIGHTCYAN_EX + "set search" + Fore.RESET + " - set if the program should search in folders")
    print("\t0 - no search, 1 - search in folders that matches filter, 2 - search all folders")
    print("\t[set search 0/1/2]\n")
    
def help_set_duplicity():
    print(Fore.LIGHTCYAN_EX + "set duplicity" + Fore.RESET + " - set if the program should show duplicity")
    print("\t[set duplicity 0/1]\n")
    
def help_set_unit():
    print(Fore.LIGHTCYAN_EX + "set unit" + Fore.RESET + " - set default size unit type")
    print("\t[set unit 0/1/2/3]")
    print("\t0 - bytes")
    print("\t1 - kilobytes")
    print("\t2 - megabytes")
    print("\t3 - gigabytes\n")

def help_show():
    print(Fore.LIGHTCYAN_EX + "show" + Fore.RESET + " - show added files\n")

def help_save():
    print(Fore.LIGHTCYAN_EX + "save" + Fore.RESET + " - save (files/added files) to variable")
    print("\t[save files/added to a]\n")

def help_load():
    print(Fore.LIGHTCYAN_EX + "load" + Fore.RESET + " - load files from txt to variable")
    print("\t[load from a.txt to variable]\n")
    
def help_input():
    print(Fore.LIGHTCYAN_EX + "input" + Fore.RESET + " - input files to the added files")
    print("\t[input] or [input file.txt]\n")
    
def help_names():
    print(Fore.LIGHTCYAN_EX + "names" + Fore.RESET + " - show all names of the files to the variable")
    print("\t[names] - print names\n\t[names variable] - put names to variable\n")
    
def help_history():
    print(Fore.LIGHTCYAN_EX + "history" + Fore.RESET + " - show history of commands")
    print("\t[history] - print history\n\t[history 0] - load history\n")
      