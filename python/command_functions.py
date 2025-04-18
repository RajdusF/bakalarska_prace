import copy
import filecmp
import json
import operator
import os
import re
import textwrap

from colorama import Fore
from tabulate import tabulate
from tqdm import tqdm

import python.global_variables as global_variables
from python.help_func import (find_name_of_browse_file, find_name_of_find_file,
                              format_time, recalculate_size, time_from_now)
from python.MyFile import XData

ops = {
    "==": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    ">": operator.gt,
    "<=": operator.le,
    ">=": operator.ge
}

def show_files(files, commands = None):
    from python.help_func import recalculate_size, time_from_now
    
    detailed_view = False
    
    if commands is not None:
        for command in commands:
            if command == "-d":
                detailed_view = True
    
    if len(files) > 1000 and detailed_view == False:    
        print(Fore.GREEN + f"Found {len(files)} files " + Fore.RESET)
        return
    
    files_info = []
        
    for file in files:
        file_size = os.path.getsize(file)
        modified_time = format_time(os.path.getmtime(file))
        created_time = format_time(os.path.getctime(file))
        
        if os.path.isdir(file):
            display_name = f"{Fore.LIGHTBLUE_EX}{file}{Fore.RESET}"
        else:
            display_name = file

        files_info.append([
            display_name,
            recalculate_size(file_size),
            modified_time,
            created_time
        ])
        
    headers = ["File", "Size", "Modified Time", "Created Time"]
    if len(files) > 0:
        print(tabulate(files_info, headers=headers, tablefmt="pretty", colalign=("left", "right", "right", "right")))
    
    """
    print(Fore.YELLOW + f"{len(files)} FILES:" + Fore.RESET)      # Number of occurrences
    for file in files:
        file_name = file.split("\\")[-1]
        file_size = os.path.getsize(file)
        is_folder = os.path.isdir(file)
        if is_folder:
            print(Fore.LIGHTBLUE_EX + f"{file_name:{global_variables.FILE_NAME_WIDTH+global_variables.SIZE_WIDTH+1}}" + Fore.RESET + f"{time_from_now(file, 'modified'):{global_variables.MODIFIED_WIDTH}} {time_from_now(file, 'created'):{global_variables.CREATED_WIDTH}}")  
        else:
            print(f"{file_name:{global_variables.FILE_NAME_WIDTH}} {recalculate_size(file_size):{global_variables.SIZE_WIDTH}} {time_from_now(file, 'modified'):{global_variables.MODIFIED_WIDTH}} {time_from_now(file, 'created'):{global_variables.CREATED_WIDTH}}")
    """

def show_added_files(added_files):
    print("Added files:")
    for file in added_files:
        file_name = file.split("\\")[-1]
        file_size = os.path.getsize(file)
        is_folder = os.path.isdir(file)
        if is_folder:
            print(Fore.LIGHTBLUE_EX + f"{file_name:{global_variables.FILE_NAME_WIDTH+global_variables.SIZE_WIDTH+1}}" + Fore.RESET + f"{time_from_now(file, 'modified'):{global_variables.MODIFIED_WIDTH}} {time_from_now(file, 'created'):{global_variables.CREATED_WIDTH}}")  
        else:
            print(f"{file_name:{global_variables.FILE_NAME_WIDTH}} {recalculate_size(file_size):{global_variables.SIZE_WIDTH}} {time_from_now(file, 'modified'):{global_variables.MODIFIED_WIDTH}} {time_from_now(file, 'created'):{global_variables.CREATED_WIDTH}}")

def add(name : str, files : list, added_files : list):
    from python.help_func import search_folder
    i = len(added_files)
    
    for file in files:
        if file.split("\\")[-1] == name:
            name = file
            break
        
    # if is folder
    if os.path.isdir(name) and name != ".":
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

def add_if_in_variables(files : list, variables : dict, variables_name : str):
    r = []
    
    for x in files:
        if x.split("\\")[-1] in variables[variables_name]:
            r.append(x)
    
    return r


def add_folder(folder : str, recursive: bool = False):
    output_files = []
    
    if not os.path.isdir(folder):
        print("Folder not found")
        return
    
    if recursive:
        for root, _, files in os.walk(folder):
            for file in files:
                output_files.append(os.path.join(root, file))
                
    else:
        for file in os.listdir(folder):
            if not os.path.isdir(os.path.join(folder, file)):
                output_files.append(os.path.join(folder, file))
        
    return output_files


def settings(option, value):
    unit = None
    search_folders = None
    show_duplicity = None
    path = None
    wraps = None
    
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
            print(Fore.RED + "Wrong input")
            
    elif option == 1:
        if value == 0:
            print("Search folders set to \"Do not search folders\"")
        elif value == 1:
            print("Search folders set to \"Search folders that matches filter\"")
        elif value == 2:
            print("Search folders set to \"Search all folders\"")
        else:
            print(Fore.RED + "Wrong input")
            return
        search_folders = value
            
    elif option == 2:
        if value == 1:
            print("Show duplicity set to True")
            show_duplicity = True
        elif value == 0:
            print("Show duplicity set to False")
            show_duplicity = False
            
    elif option == 3:
        if os.path.isdir(value):
            path = value
            print(f"Path set to {value}")
        else:
            value = value.replace("\"", "")
            value = value.replace("'", "")
            if os.path.isdir(value):
                path = value
                print(f"Path set to {value}")
            else:
                print(Fore.RED + "Path not found" + Fore.RESET)
                return
   
    elif option == 4:
        wraps = value
   
    else:
        print(Fore.RED + "Wrong input")
    
    settings_data = {}

    settings_path = os.path.join(os.path.dirname(__file__), '../settings.json')
    
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
        
    if path is not None:
        settings_data["path"] = path
        global_variables.path = path
    else:
        settings_data["path"] = global_variables.path
        
    if wraps is not None:
        settings_data["wraps"] = wraps
        global_variables.wraps = wraps
    else:
        settings_data["wraps"] = global_variables.wraps

    with open(settings_path, 'w') as json_file:
        json.dump(settings_data, json_file, indent=4)


def find(to_find : str, files : list, ignore_case : bool = False):          
    occurances = {}
    re_flags = re.IGNORECASE if ignore_case else 0
    
    output_file = find_name_of_find_file()
    
    with open("output\\" + output_file, "w") as f_output:
        for file in files:
            if not os.path.isfile(file):
                continue
            
            new = True
            file_occurances = []
            try:
                with open(file, "r", encoding="utf-8") as f:
                    for line in f:
                        if re.search(to_find, line, re_flags):
                            file_occurances.append(line.strip())
                            if new:
                                f_output.write(f"{file}\n")
                                new = False
                            f_output.write("\t" + line)
                                
                if file_occurances:
                    occurances[file] = file_occurances
            except UnicodeDecodeError:
                print(Fore.YELLOW + f"Skipping {file}: Not a valid text file." + Fore.RESET)
            except Exception as e:
                print(Fore.YELLOW + f"Skipping {file} due to error: {e}" + Fore.RESET)
            
    return occurances


def write_line_based_on_file(input_file="", input_line="", output="output/output.txt"):
    
    if not os.path.exists(output):
        with open(output, 'w') as file:
            pass
    
    with open(output, 'r+') as f:
        for line in f:
            if line.startswith("\t"):
                continue
            if line.strip() == input_file:
                f.write('\t' + input_line + '\n')
                return
        
        f.write(input_file + '\n\t' + input_line + '\n')


def sort(commands, files):
    
    r = None
    
    if commands[1] == "desc" and len(commands) == 2:
        r = sorted(files, reverse=True)
    elif commands[1] == "by" and commands[2] == "name":
        if len(commands) == 3:
            r = sorted(files)
        elif commands[3] == "desc":
            r = sorted(files, reverse=True)
    elif commands[1] == "by" and commands[2] == "size":
        if len(commands) == 3:
            r = sorted(files, key=os.path.getsize)
        elif commands[3] == "desc":
            r = sorted(files, key=os.path.getsize, reverse=True)
    elif commands[1] == "by" and commands[2] == "modified":
        if len(commands) == 3:
            r = sorted(files, key=os.path.getmtime, reverse=True)
        elif commands[3] == "desc":
            r = sorted(files, key=os.path.getmtime)
    elif commands[1] == "by" and commands[2] == "created":
        if len(commands) == 3:
            r = sorted(files, key=os.path.getctime, reverse=True)
        elif commands[3] == "desc":
            r = sorted(files, key=os.path.getctime)
    else:
        print("Wrong command")
        return []
    
    if r is not None:
        show_files(r)
        return r
        
        
def select(commands, files):
    if commands[1] == "top":
        if len(commands) == 3:
            r = files[:int(commands[2])]
            show_files(r)
            return r
    elif commands[1] == "bottom" or commands[1] == "last" or commands[1] == "bot":
            r = files[-int(commands[2]):]
            show_files(r)
            return r
    return 


def input_files(added_files, input_file="output.txt"):
    r = []
    
    if not os.path.isfile(input_file):
        print(f"File {input_file} not found")
        return
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line[-1] == '\n':
                line = line[:-1]
            added_files.append(line)
            r.append(line)
            
    print(f"Added files from {input_file}")
    
    return r


def output(added_files, extend, output_file="output.txt"):
    os.makedirs("output", exist_ok=True)  # Vytvoří složku, pokud neexistuje
    output_file = os.path.join("output", output_file)  # Přidání složky k názvu souboru
    
    if not extend and os.path.isfile(output_file):
        os.remove(output_file)
        
    with open(output_file, 'a') as f:
        for file in added_files:
            if isinstance(file, list):
                for x in file:
                    f.write(x + '\t')
                f.write('\n')
            else:
                if os.path.isfile(file):
                    f.write(file + '\n')
            
    print(f"Successfully saved to {output_file}")

    

def output_occurances(occurances, output_file="output.txt"):   
    with open(output_file, 'w') as f:
        for occurance in occurances:
            f.write(occurance[0] + '\n')
            f.write("\t" + occurance[1] + '\n')
            
    print(f"Successfully saved to {output_file}")
    
    
def set_operations(expression: str, dictionary: dict):
    words = ""
    result = []    
    temps = []
    
    open_brackets = 0
    close_brackets = 0
    
    for x in expression:
        if x == "(":
            open_brackets += 1
        elif x == ")":
            close_brackets += 1
    if open_brackets != close_brackets:
        return "ERROR"
    
    dictionary = copy.deepcopy(dictionary)
    
    while "(" in expression and ")" in expression:
            open_bracket = expression.index("(")
            close_bracket = expression.index(")")
            temps.append(set_operations(expression[open_bracket + 1:close_bracket], dictionary)) 
            
            expression = expression.replace(expression[open_bracket:close_bracket + 1], str(len(temps) - 1))
    words = expression.split(" ")
    
    dicts = words[::2]
    operations = words[1::2]
    
    while len(operations) > 0:
        operation = operations.pop(0)
        d_1 = dicts.pop(0)
        d_2 = dicts.pop(0)
        
        d_1 = temps[int(d_1)] if str(d_1).isnumeric() else dictionary[d_1]
            
        d_2 = temps[int(d_2)] if str(d_2).isnumeric() else dictionary[d_2]
    
        if operation == "U":
            for x in d_2:
                if x not in d_1:
                    d_1.append(x)
            result = d_1
        elif operation == "A":
            result = [x for x in d_1 if x in d_2]
        elif operation == "-":
            result = [x for x in d_1 if x not in d_2]
        else:
            print("ERROR")
            return
        
        dictionary["temp"] = result
        dicts.insert(0, "temp")
        
            
    if result == [] and temps != []:
        print(f"result: {temps[0]}")
        return temps[0]
    elif result != []:
        print(f"result: ")
        for x in result:
            print(x)
        return result.copy()
    else:
        return result

def save(name, output_file : str = None, shared_data = None, worker_id = None):    
    if type(name) == str and global_variables is not None and name in global_variables.variables:
        if type(global_variables.variables[name]) == XData:
            xdata = global_variables.variables[name]
            try:
                output_dir = os.getcwd()
                output_dir = os.path.join(output_dir, "output")
                
                output_filename = ""
                
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                    
                if output_file == None:
                    try:
                        output_filename = xdata.name[:xdata.name.index(".")] + ".json"
                    except:
                        output_filename = xdata.name + ".json"
                        
                elif type(output_file) == list:
                    output_filename = output_file[0]
                    
                if not output_filename.endswith(".json"):
                    if(output_filename.find(".") != -1):
                        output_filename = output_filename[:output_filename.index(".")] + ".json"
                    else:
                        output_filename = output_filename + ".json"
                
                    
                output_data = xdata.data
                
                output_filename = os.path.join(xdata.path, output_filename)
                output_filename = output_filename.replace(os.sep, '_')
                
                output_dir_file = os.path.join(output_dir, output_filename)
                
                with open(output_dir_file, "w") as json_file:
                    json.dump(output_data, json_file, indent=4)
                    
                print(f"Successfully saved to \"{output_dir_file}\"")
                return
            except Exception as e:
                print(Fore.RED + f"Error writing to file: {e}")
                return -1
            
    elif (type(name) == list and type(name[0]) == XData) or type(name) == XData:
        xdata = name
    
        if type(xdata) == list:
            for x in xdata:
                save(x, output_file, shared_data, worker_id)
        else:
            try:
                
                output_dir = os.getcwd()
                output_dir = os.path.join(output_dir, "output")
                
                output_filename = ""
                
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                    
                if output_file == None:
                    try:
                        output_filename = xdata.name[:xdata.name.index(".")] + ".json"
                    except:
                        output_filename = xdata.name + ".json"
                    
                elif type(output_file) == list:
                    output_filename = output_file[worker_id]
                    
                
                if not output_filename.endswith(".json"):
                    output_filename = output_filename[:output_filename.index(".")] + ".json"
                    
                output_data = xdata.data
                
                output_filename = os.path.join(xdata.path, output_filename)
                output_filename = output_filename.replace(os.sep, '_')
                
                output_dir_file = os.path.join(output_dir, output_filename)
                
                with open(output_dir_file, "w") as json_file:
                    json.dump(output_data, json_file, indent=4)
                    
                print(f"Successfully saved to \"{output_dir_file}\"")
                return None
            except Exception as e:
                print(Fore.RED + f"Error writing to file: {e}")
                return -1
    else:
        print(Fore.RED + f"Error during saving: Variable \"{name}\" not found" + Fore.RESET)
    
    
    
def remove(commands, added_files):
    original_length = len(added_files)
    
    if commands[1] == "*":
        added_files.clear()
        print("All files removed")
    else:
        name = commands[1]
        occurrences = []
        for x in added_files:
            if name in x:
                occurrences.append(x)
                
        
        if len(occurrences) > 1:
            for i, x in enumerate(occurrences):
                print(f"[{i}] {x}")
            inp = input("Multiple files found. Pick file to remove of \"all\" for all \"exit\" to exit: ")
            if inp == "all":
                for x in occurrences:
                    added_files.remove(x)
            elif inp == "exit":
                return
            else:
                added_files.remove(occurrences[int(inp)])
        elif len(occurrences) == 1:
            added_files.remove(occurrences[0])
            print("File removed")
        elif len(occurrences) == 0:
            print("File not found")
        
    return original_length - len(added_files)

def resolve_duplicity(files : list):
    seen_files = set()
    duplicates, unique_files = []

    for current_file in files:
        if current_file not in seen_files:
            for other_file in files:
                if other_file not in seen_files and current_file != other_file and filecmp.cmp(current_file, other_file, shallow=True):
                    duplicates.append(other_file)
                    seen_files.add(other_file)
                    print(f"{current_file.split('\\')[-1]:30} == {other_file.split('\\')[-1]:40} -> Removed {other_file.split('\\')[-1]}")
            unique_files.append(current_file)
        seen_files.add(current_file)
    
    return unique_files, duplicates