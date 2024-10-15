import json
import os

from colorama import Fore

import global_variables
from command_functions import filter


def help():
    print(Fore.YELLOW)
    print("Commands:")
    print("filter - filter a files based on specification [find name output.txt] or [find name output.txt size < 100]")
    print("add - add a files from filtered list [add file.txt] or [add *]")
    print("remove - remove a file from the list of files to be processed [remove file.txt]")
    print("set unit - set default unit for size [set unit KB]")
    print("set search - set if the program should search in folders [set search 0/1]")
    print("exit - exit the program")
    
    print("\nTo set default size unit type 'set unit [unit]'")
    print("0 - bytes")
    print("1 - kilobytes")
    print("2 - megabytes")
    print("3 - gigabytes")
    print(Fore.RESET)
    
    
def read_json(file):    
    with open(file) as json_file:
        data = json.load(json_file)
        
    global_variables.default_unit = data["unit"]
    
    if data["search_folders"] == True:
        global_variables.search_folders = True
    else:
        global_variables.search_folders = False    


def recalculate_size(size: int, unit: str) -> int:
    if unit == "KB":
        return size / 1024
    elif unit == "MB":
        return size / 1024 / 1024
    elif unit == "GB":
        return size / 1024 / 1024 / 1024
    return size


def search_folder(folder):
    absolute_paths = []
    for file in os.listdir(folder):
        is_folder = os.path.isdir(folder + '\\' + file)
        if is_folder == True:
            absolute_paths.extend(search_folder(folder + '\\' + file))
        else:
            absolute_paths.append(os.path.abspath(folder + '\\' + file))
                
    return absolute_paths


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