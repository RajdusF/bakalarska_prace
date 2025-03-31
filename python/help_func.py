import datetime
import glob
import importlib
import inspect
import json
import os
import re
import sys
import textwrap
import time

from colorama import Fore, Style, init
from tabulate import tabulate

path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'python'))
if path not in sys.path:
    sys.path.append(path)


import python.command_functions as command_functions
import python.custom_functions
import python.file_handling as file_handling
import python.global_variables as global_variables
import python.parallel_for
import python.parallel_for as parallel_for

custom_functions = importlib.import_module('python.custom_functions')
paralell_functions = importlib.import_module('python.parallel_for')
file_handling_functions = importlib.import_module('python.file_handling')
command_functions_functions = importlib.import_module('python.command_functions')

history = []

def execute_command(command, variables):
    globals()["write_line_based_on_file"] = command_functions.write_line_based_on_file
    
    for name, func in inspect.getmembers(custom_functions, inspect.isfunction):
        globals()[name] = func
    for name, func in inspect.getmembers(paralell_functions, inspect.isfunction):
        globals()[name] = func
    for name, func in inspect.getmembers(file_handling_functions, inspect.isfunction):
        globals()[name] = func
    for name, func in inspect.getmembers(command_functions_functions, inspect.isfunction):
        globals()[name] = func
    
    try:
        result = eval(command, globals(), locals())
        return result
    except SyntaxError:
        try:
            exec(command, globals(), locals())
        except Exception as e:
            print(Fore.RED + f"Exec error: {e}")
    except Exception as e:
        print(Fore.RED + f"Eval error: {e}")

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
            
        # print(f"Number {position}: {numbers[position]}")
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
            
        # print(f"Number {position}: {numbers[position]}")
        return numbers[position]
    except:
        return None

def wrap_text(text, width):
    return "\n".join(textwrap.wrap(str(text), width))

def print_occurances(occurances : dict):
    
    s = ""
    total_occurances = 0
    
    for key, values in occurances.items():
        s += f"{key}\n"
        for value in values:
            s += f"\t{value}\n"
            total_occurances += 1
        s += "\n"
        
    print(Fore.GREEN + f"Found {total_occurances} occurances:" + Fore.RESET)
    print(s)
                    
    # temp_occurences = []
    # for i, occurance in enumerate(files):
    #     name, line = None, None
    #     name = occurance[0]
    #     line = occurance[1]
            
    #     temp_occurences.append([i, name, line])
    # headers = ["Index", "File path", "Line"]

    # data_wrapped = []
    # for row in temp_occurences:
    #     wrapped_row = [wrap_text(cell, global_variables.wraps[col]) for col, cell in enumerate(row)]
    #     data_wrapped.append(wrapped_row)
    
    # table = tabulate(data_wrapped, headers=headers, tablefmt="grid")
    # print(table)

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
    
    if os.path.isdir(data["path"]):
        global_variables.path = data["path"]
    else:
        global_variables.path = os.getcwd()
    
    global_variables.wraps = data["wraps"]

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
        commands = []
        current_command = ""

        with open("configurator_commands.txt", "r") as file:
            for line in file:
                if line.startswith("#") or line == "\n" or line == "":
                    continue
                
                stripped = line.rstrip()

                if current_command:
                    if stripped and (stripped[0] == " " or stripped[0] == "\t"):
                        current_command += "\n" + stripped
                    else:
                        commands.append(current_command)
                        current_command = stripped
                else:
                    current_command = stripped
                
            if current_command:
                commands.append(current_command)
        
        return commands

    except FileNotFoundError:
        print(Fore.RED + "The file 'configurator_commands.txt' does not exist" + Fore.RESET)
        return None
    
def find_name_of_browse_file():
    # list of files
    files = os.listdir("output")
    
    max = 0
    
    for file in files:
        if file.startswith("browse_output"):
            file = file.split(".")[0]
            if len(file.split("_")) == 3:
                num = int(file.split("_")[2])
                if num >= max:
                    max = num + 1
    
    return "browse_output_" + str(max) + ".txt"

def find_name_of_find_file():
    # list of files
    files = os.listdir("output")
    
    max = 0
    
    for file in files:
        if file.startswith("find_output"):
            file = file.split(".")[0]
            if len(file.split("_")) == 3:
                num = int(file.split("_")[2])
                if num >= max:
                    max = num + 1
    
    return "find_output_" + str(max) + ".txt"

def comments_removal(string : str) -> str:
    last_end_mark = 0
    if "#" in string:
        for i, x in enumerate(string):
            if x == "#":
                first_mark = -1
                second_mark = -1
                if "\"" in string:
                    first_mark = string.find("\"", last_end_mark + 1)
                    second_mark = string.find("\"", first_mark + 1)
                    last_end_mark = second_mark
                
                    if first_mark != -1 or second_mark != -1:
                        if first_mark < str(string). index("#") < second_mark:
                            pass
                        else:
                            string = string[:i]
                        
                else:
                    string = string[:string.index("#")]
                    
    return string.strip()
    
def convert_variables_to_variables_from_dict(string: str, variables: dict) -> str:
    last_text = ""
    def replace_match(match):
        global last_text
        text = match.group(0)
        
        if text.startswith('"') and text.endswith('"') and last_text != "f":
            return text

        for key, value in variables.items():
            text = re.sub(rf'\b{re.escape(key)}\b', f'variables["{key}"]', text)
            
        last_text = text
        return text

    # Zavolat replace pro každý výskyt
    string = re.sub(r'("[^"]*"|\b\w+\b)', replace_match, string)

    return string
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
    help_set_unit()
    help_set_search()
    help_set_duplicity()
    help_set_path()
    
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
    # print("You can use regular expressions like - BEFORE EVERY EXPRESSION MUST BE \"\\\": \n\t\\b (bounderies) - for finding whole words \n\t\t[find \"\\bMolecule\\b\"] - will find only \"Molecule\" without \"Molecules\" ...\n")
    print("You can use regular expressions like: \n\t\\b (bounderies) - for finding whole words \n\t\t[find \"\\bMolecule\\b\"] - will find only \"Molecule\" without \"Molecules\" ...\n")
    print("\t^ - start of the line (Alt + 94) \n\t\t[find \"^#\"] - will find all lines starting with \"#\"")
    print("\t\t[find \"^(?!#).+\"]\" - will find all lines that are not comments\n")
    print("\t\d - digit \n\t\t[find \"\\d\"] - will find all lines with digits")
    print("\t\t[find \"\b\d+\b\"] - will find all lines digit that are not part of alfanumeric strings\n")
    print("\tYou can use flag -I for case insensitive search\n\t\t[find \"bnx\" in added -I]\n")


    
def help_take_int():
    print(Fore.LIGHTCYAN_EX + "take_int" + Fore.RESET + " - take integer from the message (made for occurances after command \"find\")")
    print("\t[take_int(lines, 0) > 6000] - browsing in column with text or [take_int(file, 0)] - browsing in column with file path/file name\n")

def help_take_float():
    print(Fore.LIGHTCYAN_EX + "take_float" + Fore.RESET + " - take float from the message (made for occurances after command \"find\")")
    print("\t[take_float(lines, 0) > 6000,50] - browsing in column with text or [take_float(file, 0)] - browsing in column with file path/file name\n")
      
def help_output():
    print(Fore.LIGHTCYAN_EX + "output" + Fore.RESET + " - output added files to text file")
    print("\t[output file.txt] or [output file.txt extend] - to extend the output file\n")
    print("\t[output occ/occurances file.txt] - output occurances to text file\n")
    
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
    
def help_set_path():
    print(Fore.LIGHTCYAN_EX + "set path" + Fore.RESET + " - set path to the folder")
    print("\t[set path \"C:\\Users\\Documents\"]\n")

def help_show():
    print(Fore.LIGHTCYAN_EX + "show" + Fore.RESET + " - show added files\n")

def help_save():
    print(Fore.LIGHTCYAN_EX + "save" + Fore.RESET + " - save (files/added files/occurances - file names) to variable")
    print("\t[save files/added/occurances variable]\n")

def help_load():
    print(Fore.LIGHTCYAN_EX + "load" + Fore.RESET + " - load added files from txt to variable")
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
      
def debug_write(message):
    with open("debug.txt", "a") as file:
        file.write(f"{message}\n")