import filecmp
import glob
import os
import time

from colorama import Fore

import global_variables
from help_func import recalculate_size, search_folder


def filter(commands):

    size = None
    operator = None
    name = None
    modified = None
    modified_operator = None
    time_unit = None
    duplicates = []
    
    if "name" in commands:
        name_index = commands.index("name") + 1
        if name_index < len(commands):
            name = commands[name_index]    
    elif commands[commands.index("filter") + 1] == "*":
        name = "*"            
                    
    if "size" in commands:
        operator_index = commands.index("size") + 1
        if operator_index < len(commands):
            operator = commands[operator_index]
            size_index = operator_index + 1
            if size_index < len(commands):
                size = int(commands[size_index])
                
    # filter modified < 10 days
    if "modified" in commands:
        modified_operator = commands[commands.index("modified") + 1]
        if commands.index("modified") + 1 < len(commands):
            modified = int(commands[commands.index("modified") + 2])
            if commands.index("modified") + 2 < len(commands):
                time_unit = commands[commands.index("modified") + 3]
        if modified_operator == None or modified == None or time_unit == None:
            print("Wrong input")
            return
        
        print(f"modified_operator: {modified_operator} ; modified: {modified} ; time_unit: {time_unit}")
                
                
    if name == None and size == None and modified == None:
        print("Wrong input")
        return
    
    if name:
        if "name" in commands and commands[commands.index("name") - 1] == "not":
            all_files = glob.glob(global_variables.path + "\\*", recursive=True)
            name_files = glob.glob(global_variables.path + "\\" + name, recursive=True)
            files = [file for file in all_files if file not in name_files]
        else:
            files = glob.glob(global_variables.path + "\\" + name, recursive=True)
    else:
        files = glob.glob(global_variables.path + "\\*", recursive=True)
        
    files_from_folders = []
    
    if global_variables.search_folders:
        for file in files:
            is_folder = os.path.isdir(file)
            if is_folder:
                files_from_folders.extend(search_folder(file))
        
    if size and operator and commands[commands.index("size") - 1] != "not":
        if operator == "<":
            files = [file for file in files if os.path.getsize(file) < size]
        elif operator == "<=":
            files = [file for file in files if os.path.getsize(file) <= size]
        elif operator == ">":
            files = [file for file in files if os.path.getsize(file) > size]
        elif operator == ">=":
            files = [file for file in files if os.path.getsize(file) >= size]
        elif operator == "=":
            files = [file for file in files if os.path.getsize(file) == size]
    elif size and operator and commands[commands.index("size") - 1] == "not":
        if operator == "<":
            files = [file for file in files if os.path.getsize(file) >= size]
        elif operator == "<=":
            files = [file for file in files if os.path.getsize(file) > size]
        elif operator == ">":
            files = [file for file in files if os.path.getsize(file) <= size]
        elif operator == ">=":
            files = [file for file in files if os.path.getsize(file) < size]
        elif operator == "=":
            files = [file for file in files if os.path.getsize(file) != size]
    
    #           m_operator modified time_unit
    # filter modified < 10 days
    if modified and modified_operator and time_unit: 
        if time_unit == "s" or time_unit == "second" or time_unit == "seconds" or time_unit == "sec":
            n = 1
        elif time_unit == "m" or time_unit == "minute" or time_unit == "minutes" or time_unit == "min":
            n = 60
        elif time_unit == "h" or time_unit == "hour" or time_unit == "hours" or time_unit == "hr":
            n = 60 * 60
        elif time_unit == "d" or time_unit == "day" or time_unit == "days":
            n = 24 * 60 * 60
        elif time_unit == "w" or time_unit == "week" or time_unit == "weeks":
            n = 7 * 24 * 60 * 60
        elif time_unit == "m" or time_unit == "month" or time_unit == "months":
            n = 30 * 24 * 60 * 60
        elif time_unit == "y" or time_unit == "year" or time_unit == "years":
            n = 365 * 24 * 60 * 60
        else:
            print("Wrong time unit")
            return
        
        current_time = time.time()
        
        temp_files = files.copy()
        files.clear()
        
        for file in temp_files:
            modification_time = os.path.getmtime(os.path.join(file))
            seconds_from_now = current_time - modification_time
            print("File: ", file.split("\\")[-1])
            print("Seconds from now: ", seconds_from_now)
            print("Hours from now: ", seconds_from_now / 3600, "\n")
            print("Days from now: ", seconds_from_now / 3600 / 24, "\n")
        
            if modified_operator == "<":
                if seconds_from_now / n < modified:
                    files.append(file)
            elif modified_operator == "<=":
                if seconds_from_now / n <= modified:
                    files.append(file)
            elif modified_operator == ">":
                if seconds_from_now / n > modified:
                    files.append(file)
            elif modified_operator == ">=":
                if seconds_from_now / n >= modified:
                    files.append(file)
            elif modified_operator == "=":
                if seconds_from_now / n == modified:
                    files.append(file)


    if global_variables.show_duplicity:
        temp = files.copy()
        files.clear()
        seen_files = set()
        duplicates = []

        for x in temp:
            if x not in seen_files:
                for i in temp:
                    if i not in seen_files and x != i and filecmp.cmp(x, i, shallow=True):
                        duplicates.append(i)
                        seen_files.add(i)
                        print(f"{x.split('\\')[-1]:30} == {i.split('\\')[-1]:40} -> Removed {i.split('\\')[-1]}")
                files.append(x)
            seen_files.add(x)
            
                
    print(Fore.GREEN + f"Found {len(files)} files:" + Fore.RESET)      # Number of occurances
    for file in files:
        file_name = file.split("\\")[-1]
        file_size = os.path.getsize(file)
        is_folder = os.path.isdir(file)
        if is_folder and modified and modified_operator and time_unit:
            print(f"{file_name:35}  {time.ctime(os.path.getmtime(file))}")
        elif is_folder:
            print(f"{file_name:35}")
        elif modified and modified_operator and time_unit:
            print(f"{file_name:35} {str(recalculate_size(file_size, global_variables.default_unit))} {global_variables.default_unit} {time.ctime(os.path.getmtime(file))}")
        else:
            print(f"{file_name:35} {str(recalculate_size(file_size, global_variables.default_unit))} {global_variables.default_unit}")
            
    if global_variables.show_duplicity == True:
        print(Fore.RED + f"Found {len(duplicates)} duplicates:" + Fore.RESET)
        for duplicate in duplicates:
            file_name = duplicate.split("\\")[-1]
            file_size = os.path.getsize(duplicate)
            print(f"{file_name:35} {str(recalculate_size(file_size, global_variables.default_unit))} {global_variables.default_unit}")
                
    return files