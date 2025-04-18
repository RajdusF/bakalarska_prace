import os
import time
from pathlib import Path

from colorama import Fore
from tabulate import tabulate

import python.global_variables as global_variables
import python.global_variables as g
from python.command_functions import (add_if_in_variables, resolve_duplicity,
                                      show_files)
from python.help_func import (format_time, parse_time, progress_bar,
                              recalculate_size, search_folder, time_from_now)

FILE_NAME_WIDTH = 48
SIZE_WIDTH = 18
MODIFIED_WIDTH = 16
CREATED_WIDTH = 16


def filter(command, commands, input_files = None, input_added_files = None, dict = None):
    # Inicialization
    size = None
    size_operator = None
    size_unit = None
    name = None
    modified = None
    modified_operator = None
    modified_time_unit = None
    created = None
    created_operator = None
    created_time_unit = None
    max_files = None
    num_of_folders = 0
    duplicates = []
    files = []
    only_directories = []
    g.status = ""
    
    if "-MAX:" in command:
        max_files = int(command.split("-MAX:")[1].split()[0])
        command = command.replace(f"-MAX:{max_files}", "")
        commands.remove(f"-MAX:{max_files}")
    
    # Searching for name, size, modified
    if "name" in commands:
        name_index = commands.index("name") + 1
        if name_index < len(commands):
            name = commands[name_index]    
    elif commands[commands.index("filter") + 1] == "*":
        name = "*"            
                    
    if "size" in commands:
        operator_index = commands.index("size") + 1
        if operator_index < len(commands):
            size_operator = commands[operator_index]
            size_index = operator_index + 1
            if size_index < len(commands):
                size = int(commands[size_index])
                if size_index + 1 < len(commands):
                    size_unit = commands[size_index + 1]
                
    if "modified" in commands:
        modified_operator = commands[commands.index("modified") + 1]
        if commands.index("modified") + 2 < len(commands) and "/" in commands[commands.index("modified") + 2]:
            modified = commands[commands.index("modified") + 2]
            
            if modified == None or modified_operator == None:
                print(Fore.RED + "Wrong input")
                return
        elif commands.index("modified") + 1 < len(commands):
            try:
                modified = float(commands[commands.index("modified") + 2])
            except:
                print(Fore.RED + "Wrong input")
                return
            if commands.index("modified") + 2 < len(commands):
                modified_time_unit = commands[commands.index("modified") + 3]
                
            if modified_operator == None or modified == None or modified_time_unit == None:
                print(Fore.RED + "Wrong input")
                return
        
        
    if "created" in commands:
        created_operator = commands[commands.index("created") + 1]
        if commands.index("created") + 1 < len(commands):
            created = float(commands[commands.index("created") + 2])
            if commands.index("created") + 2 < len(commands):
                created_time_unit = commands[commands.index("created") + 3]
        if created_operator == None or created == None or created_time_unit == None:
            print(Fore.RED + "Wrong input")
            return
            
    
    if commands[1] == "files" or commands[1] == "added_files" or commands[1] == "added":
        temp = []
        if commands[1] == "files":
            temp = input_files.copy()
        elif commands[1] == "added_files" or commands[1] == "added":
            temp = input_added_files.copy()
            
        if name and "not" in commands:
            for x in temp:
                if not filter_by_name(x, name):
                    files.append(x)
        elif name:
            for x in temp:
                if filter_by_name(x, name):
                    files.append(x)
        else:
            files = temp.copy()
    
        
        if global_variables.search_folders == 1:
            for folder in os.isdir(input_files):
                if name in folder:
                    temp_files, num_of_folders = search_folder(folder, commands)
                    files.extend(temp_files)
                    g.status = f"filter: Currently {len(files)} files"
        elif global_variables.search_folders == 2:            
            progress_bar(0, 100, 30)
            all_directories = [file for file in input_files if os.path.isdir(file)]    
            
            for i, folder in enumerate(all_directories):
                temp_files, num_of_folders_returned = search_folder(folder=folder, commands=commands, progress=i, progress_total=len(all_directories))
                num_of_folders += num_of_folders_returned
                files.extend(temp_files)
                g.status = f"filter: Currently {len(files)} files"
                progress_bar(i, len(all_directories), 30)
                
            progress_bar(1, 1, 30)
            print()
                
                
        num_of_folders += len(only_directories)
        
        input_files.clear()
        
        if max_files != None:
            files = files[:max_files]
        
    else:
        input_files.clear()
        
        # TODO: if path is not set, warning and return
        if global_variables.path == None or global_variables.path == "":
            print(Fore.RED + "Path is not set for filtering" + Fore.RESET)
            return []
        
        if name == None and size == None and modified == None and created == None:
            print(Fore.RED + "Wrong input")
            return []
        
        # NAME
        if name:
            path = Path(global_variables.path)

            if "name" in commands and commands[commands.index("name") - 1] == "not":  # NOT NAME
                all_files = list(path.glob("*"))
                name_files = list(path.glob(name))
                
                all_files = [str(file) for file in all_files]
                name_files = [str(file) for file in name_files]

                files = [file for file in all_files if file not in name_files]

                only_directories = [d for d in map(Path, files) if d.is_dir()]

            else:  # NAME
                files = list(path.glob(name))
                files = [str(file) for file in files]


                only_directories = [d for d in map(Path, files) if d.is_dir()]

        else:  # NO NAME
            files = list(path.glob("*"))
            files = [str(file) for file in files]

            print(f"in else: {files}")

            only_directories = [d for d in map(Path, files) if d.is_dir()]
            
        
        if global_variables.search_folders == 1:
            for folder in only_directories:
                if max_files != None and len(files) >= max_files:
                    break
                temp_files, num_of_folders = search_folder(folder, commands)
                files.extend(temp_files)
        elif global_variables.search_folders == 2:            
            progress_bar(0, 100, 30)
            all_directories = [os.path.abspath(entry.path) for entry in os.scandir(global_variables.path) if entry.is_dir()]        
            
            for i, folder in enumerate(all_directories):
                if max_files != None and len(files) >= max_files:
                    break
                temp_files, num_of_folders_returned = search_folder(folder=folder, commands=commands, progress=i, progress_total=len(all_directories))
                num_of_folders += num_of_folders_returned
                files.extend(temp_files)
                progress_bar(i, len(all_directories), 30)
                
            progress_bar(1, 1, 30)
            print()
                
                
        num_of_folders += len(only_directories)
        
   
    # command = filter name *.txt size > 100KB contains names1 (dict)
    if "contains" in commands:
        contains_name = commands[commands.index("contains") + 1]
        files = add_if_in_variables(files, dict, contains_name)
    
    
    if size and size_operator:
        files = filter_size(files, size_operator, size, size_unit)
        

    #           m_operator modified time_unit
    # filter modified < 10 days
    if modified and modified_operator and modified_time_unit or "/" in modified and modified_operator: 
        files = filter_time(files, modified_operator, modified, modified_time_unit, "modified")
        
    if created and created_operator and created_time_unit: 
        files = filter_time(files, created_operator, created, created_time_unit, "created")

    if global_variables.show_duplicity:
        files_temp = files.copy()
        files.clear()
        
        files, duplicates = resolve_duplicity(files_temp)
    
    if max_files != None:
        files = files[:max_files]
        num_of_folders = 0
        for x in files:
            if os.path.isdir(x):
                num_of_folders += 1
        
    
    if len(files) > 1000:
        commands.append("-h")        
    
    if "-h" in commands:        # hide
        print(Fore.GREEN + f"Found {len(files) - num_of_folders} files and {num_of_folders} folders:" + Fore.RESET)
    else:
        print(Fore.GREEN + f"Found {len(files) - num_of_folders} files and {num_of_folders} folders:" + Fore.RESET)      # Number of occurances
        
        show_files(files)
        
        """
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
        print(tabulate(files_info, headers=headers, tablefmt="pretty"))
        """
        
        """
        if "-d" in commands:        # detailed
            print(f"{'file':{FILE_NAME_WIDTH+4}} {'size':{SIZE_WIDTH}} {'modified':{MODIFIED_WIDTH}} {'created':{CREATED_WIDTH}}")
        for file in files:
            file_name = file.split("\\")[-1]
            is_folder = os.path.isdir(file)
            
            if "-d" in commands and not is_folder:
                print(f"{file_name:{FILE_NAME_WIDTH}} {recalculate_size(file_size):{SIZE_WIDTH}} {time_from_now(file, 'modified'):{MODIFIED_WIDTH}} {time_from_now(file, 'created'):{CREATED_WIDTH}}")
            elif "-d" in commands and is_folder:
                print( Fore.LIGHTBLUE_EX + f"{file_name:{FILE_NAME_WIDTH+SIZE_WIDTH+1}}", end="" )
                print(f"{time_from_now(file, 'modified'):{MODIFIED_WIDTH}} {time_from_now(file, 'created'):{CREATED_WIDTH}}")
            else:
                if is_folder:
                    print(Fore.LIGHTBLUE_EX + f"{file_name:{FILE_NAME_WIDTH}}", end="")
                else:  
                    print(f"{file_name:{FILE_NAME_WIDTH}}", end="")
                if size and size_operator and not is_folder:
                    print(f"{recalculate_size(file_size):{SIZE_WIDTH}}", end="")
                else:
                    print(" " * 14, end="")
                if modified and modified_operator and modified_time_unit:
                    print(f"{time_from_now(file, "modified"):{MODIFIED_WIDTH}}", end="")
                if created and created_operator and created_time_unit:
                    print(f"{time_from_now(file, "created"):{CREATED_WIDTH}}", end="")
                print()
        """    
            
    if global_variables.show_duplicity == True:
        print(Fore.RED + f"Found {len(duplicates)} duplicates:" + Fore.RESET)
        for duplicate in duplicates:
            file_name = duplicate.split("\\")[-1]
            file_size = os.path.getsize(duplicate)
            print(f"{file_name:35} {recalculate_size(file_size):13}")
    
    return files, duplicates


def filter_time(in_files, modified_operator, modified, time_unit, option):
    out_files = []
    
    
    if "/" in modified and time_unit == None:
        modified = parse_time(modified)
        for file in in_files:
            if option == "modified":
                comparision_time = os.path.getmtime(os.path.join(file))
            elif option == "created":
                comparision_time = os.path.getctime(os.path.join(file))

            if modified_operator == ">":
                if comparision_time > modified:
                    out_files.append(file)
            elif modified_operator == ">=":
                if comparision_time >= modified:
                    out_files.append(file)
            elif modified_operator == "<":
                if comparision_time < modified:
                    out_files.append(file)
            elif modified_operator == "<=":
                if comparision_time <= modified:
                    out_files.append(file)
            elif modified_operator == "=" or modified_operator == "==":
                if modified == comparision_time:
                    out_files.append(file)
    else:
        current_time = time.time()
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
        
        
        for file in in_files:
            if option == "modified":
                modification_time = os.path.getmtime(os.path.join(file))
                seconds_from_now = current_time - modification_time
            elif option == "created":
                created_time = os.path.getctime(os.path.join(file))
                seconds_from_now = current_time - created_time
        
            if modified_operator == "<":
                if seconds_from_now / n < modified:
                    out_files.append(file)
            elif modified_operator == "<=":
                if seconds_from_now / n <= modified:
                    out_files.append(file)
            elif modified_operator == ">":
                if seconds_from_now / n > modified:
                    out_files.append(file)
            elif modified_operator == ">=":
                if seconds_from_now / n >= modified:
                    out_files.append(file)
            elif modified_operator == "=":
                if seconds_from_now / n == modified:
                    out_files.append(file)
                
    return out_files


def filter_size(in_files, size_operator, size, size_unit=None):
    out_files = []
    
    if size_unit == "B" or size_unit == "byte" or size_unit == "bytes":
        size = size
    elif size_unit == "KB" or size_unit == "kilobyte" or size_unit == "kilobytes":
        size = size * 1024
    elif size_unit == "MB" or size_unit == "megabyte" or size_unit == "megabytes":
        size = size * 1024 * 1024
    elif size_unit == "GB" or size_unit == "gigabyte" or size_unit == "gigabytes":
        size = size * 1024 * 1024 * 1024
        
    
    for file in in_files:
        file_size = os.path.getsize(file)
        
        if size_operator == "<":
            if file_size < size:
                out_files.append(file)
        elif size_operator == "<=":
            if file_size <= size:
                out_files.append(file)
        elif size_operator == ">":
            if file_size > size:
                out_files.append(file)
        elif size_operator == ">=":
            if file_size >= size:
                out_files.append(file)
        elif size_operator == "=":
            if file_size == size:
                out_files.append(file)
                
    return out_files


def filter_by_name(file : str, find : str) -> bool:
    file = file.lower()
    find = find.lower()
    
    if "\\" in file:
        file = file.split("\\")[-1]

    if "*" not in find and "?" not in find:
        return file == find
    elif find == "*":
        return True

    file_index, find_index, last_star_index = 0, 0, -1

    while file_index < len(file):
        if find_index < len(find) and (find[find_index] == "?" or find[find_index] == file[file_index]):
            file_index += 1
            find_index += 1
        elif find_index < len(find) and find[find_index] == "*":
            last_star_index = find_index
            find_index += 1
            last_match_index = file_index
        elif last_star_index != -1:
            find_index = last_star_index + 1
            last_match_index += 1
            file_index = last_match_index
        else:
            return False

    while find_index < len(find) and find[find_index] == "*":
        find_index += 1

    return find_index == len(find)