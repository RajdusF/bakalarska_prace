import os
from pprint import pprint

from colorama import Fore
from tabulate import tabulate

import python.global_variables as global_variables
from python.command_functions import (add, add_folder, add_if_in_variables,
                                      find, input_files, output,
                                      output_occurances, remove, save, select,
                                      set_operations, settings, show_files,
                                      sort)
from python.file_handling import load
from python.global_variables import find_occurances as find_occurances
from python.global_variables import result as result
from python.help_func import (add_history,
                              convert_variables_to_variables_from_dict,
                              execute_command, get_variable, help_add, help_cd,
                              help_filter, help_find, help_output, help_save,
                              help_select, help_sort, help_take_float,
                              help_take_int, load_history, my_help,
                              print_history, print_occurances,
                              show_added_files, show_current_folder,
                              take_float, take_int)


def process_command(command : str, variables, files : list, added_files : list):
    from python.filter import filter
    global find_occurances
    global result
    
    command = command.strip()
    commands = command.split(" ")
    original_command = command
    
    # Processing conditions
    if "if" in command and "(" in command and ")" in command and "{" in command and "}" in command:
        if_condition = command[command.index("(") + 1:command.index(")")]
        statement = command[command.index("{") + 1:command.index("}")]
        statements = statement.split(";")
        
        try:
            if eval(if_condition):
                for s in statements:
                    process_command(s, variables, files, added_files)
        except:
            if process_command(statement, variables, files, added_files):
                for s in statements:
                    process_command(s, variables, files, added_files)
            
    else:
        # Trying to get variable
        try:
            temp = None
            temp = get_variable(command, find_occurances)
            if temp != None:
                result.clear()
                result.extend(temp)
                print("To save result use \"save result to variable/file.txt\"")
                print("Result:")
                for x in result:
                    print(x)
        except:
            if command == "exit":
                return -1
            
            if command == "?" or command == "help":
                my_help()
                return
            
            if commands[0] == "print":
                try:
                    result = get_variable(command, find_occurances)
                    for x in result:
                        print(x)
                except:
                    print(command[6:])
                return
            
            if "**" in command:
                print(Fore.RED + "Wrong input")
                return
            
            if command == "*" or command == "ls":
                show_current_folder()
                
            # b = 5     Variables...
            elif len(commands) > 2 and commands[1] == "=":
                variables[commands[0]] = process_command(command[command.index("=") + 1:], variables, files, added_files)
                if commands[0] in variables:
                    print(f"Variable \"{commands[0]}\" saved")
                else:
                    print(Fore.RED + "Error during saving variable")
            elif command == "":
                return
  
            elif command == "cd.." or command == "cd ..":
                global_variables.path = os.path.abspath(os.path.join(global_variables.path, os.pardir))
                print(f"Current path: {global_variables.path}")
                
            elif "cd" in command:
                path_index = commands.index("cd") + 1
                
                if global_variables.path == None:
                    global_variables.path = ""
                
                if path_index < len(commands):
                    path = commands[path_index]
                    if os.path.isdir(path) and "\\" in path or "/" in path:
                        global_variables.path = path
                        print(f"Current path: {global_variables.path}")
                        settings(3, global_variables.path)
                    elif os.path.isdir(global_variables.path + "\\" + path):
                        global_variables.path = global_variables.path + "\\" + path
                        print(f"Current path: {global_variables.path}")
                        settings(3, global_variables.path)
                    else:
                        print(Fore.RED + "Path not found" + Fore.RESET)
                else:
                    print(f"Current path: {global_variables.path}")
                    
                if commands[0] == "cd" and len(commands) == 1:
                    help_cd()
                    
            elif "filter" in commands:
                if commands[0] == "filter" and len(commands) == 1:
                    help_filter()
                    return
                
                temp = filter(command, commands, files, added_files, variables)
                files.clear()
                files.extend(temp)
                
                add_history(command, files)
                
                return files.copy()
            
            elif "sort" in commands:
                if commands[0] == "sort" and len(commands) == 1:
                    help_sort()
                    return
                
                temp = sort(commands, files)
                files.clear()
                files.extend(temp)
                add_history(command, files)
                
            elif "select" in commands:
                if commands[0] == "select" and len(commands) == 1:
                    help_select()
                    return
                
                temp = select(commands, files)
                files.clear()
                files.extend(temp)
                add_history(command, files)
            
            elif commands[0] == "find":
                if len(commands) == 1:
                    help_find()
                    return
                find_occurances.clear()
                
                first_mark = command.index("\"")
                second_mark = command.index("\"", first_mark + 1)
                
                to_find = command[first_mark + 1:second_mark]
                
                if to_find == "":
                    print(Fore.RED + "Finding interrputed - no string to find")
                    return
                
                command = command.replace("\""+to_find+"\"", "").strip()
                commands = command.split(" ")
                
                ignore_case = False
                if "-I" in commands:
                    ignore_case = True
                
                if len(commands) > 3:
                    if commands[2] == "in" and commands[3] == "files":
                        if len(files) == 0:
                            print(Fore.RED + "0 files to search in")
                            return
                        find_occurances = find(to_find, files, ignore_case)
                    elif commands[2] == "in" and commands[3] == "added":
                        if len(added_files) == 0:
                            print(Fore.RED + "0 files to search in")
                            return
                        find_occurances = find(to_find, added_files, ignore_case)
                else:
                    if len(files) == 0:
                        print(Fore.RED + "0 files to search in")
                        return
                    find_occurances = find(to_find, files, ignore_case)
                    
                print_occurances(find_occurances)              
                files.clear()
                files.extend(list(find_occurances.keys()))
                
                add_history(original_command, files, find_occurances)
                
                            
            elif "add" in commands and len(commands) > 1:
                if commands[0] == "add" and len(commands) == 1:
                    help_add()
                    return
                
                if commands[1] == "occ" or commands[1] == "occurances" and len(commands) == 2:
                    added_files.extend([x[0] for x in find_occurances])
                elif commands[1] == "files" and commands[2] == "contains":
                    r = add_if_in_variables(files, added_files, variables, commands[3])
                    for file in r:
                        if file not in added_files:
                            added_files.append(file)
                
                elif commands[1] == "*" and len(commands) == 2:
                    add("*", files, added_files)
                elif "\\" in command and len(commands) == 2:
                    if os.path.isdir(commands[1]):
                        added_files.extend(add_folder(commands[1]))
                    elif os.path.isfile(commands[1]):
                        added_files.append(commands[1])
                    else:
                        print(Fore.RED + "File not found")
                    
                elif len(commands) == 2:
                        name = commands[1]
                        add(name, files, added_files)
                else:
                    print(Fore.RED + "Wrong input")
                    return
                
                print(f"Added files ({len(added_files)}):")
                for x in added_files:
                    print(x)
                    
            elif "remove" in commands:
                r = remove(commands, added_files)
                print(f"Removed {r} files")
                    
            elif command == "files":
                show_files(files)
            elif command == "added":
                show_added_files(added_files)
            
            elif "show" in commands:
                if len(commands) == 2 and commands[1] == "added":
                    show_added_files(added_files)
                elif len(commands) == 2 and commands[1] == "files":
                    show_files(files)
                elif len(commands) == 2 and commands[1] == "dist":
                    print(variables)
                elif len(commands) == 2:                          # variables[commands[1]]):
                    if variables.get(commands[1]) != None:
                        print(f"Files in \"{commands[1]}\":")
                        for x in variables[commands[1]]:
                            print(x)
                    else:
                        print(f"Save file {commands[1]} not found")
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
                elif "wraps" in commands and len(commands) == 3:
                    settings(4, [commands[2], commands[3], commands[4]])
                elif len(commands) == 1:
                    print(f"Default unit: {global_variables.default_unit}")
                    print(f"Search folders: {global_variables.search_folders}")
                    print(f"Show duplicity: {global_variables.show_duplicity}")
                    print(f"Wraps (column widths): {global_variables.wraps}")
                    return
        
            # save [result/files/names/added/occurances] [file]
            elif commands[0] == "save":
                if len(commands) == 1:
                    help_save()
                if len(commands) == 3:
                    if commands[1] == "result":
                        variables[commands[2]] = result.copy()
                        print(f"Result saved to \"{commands[2]}\"")
                    elif commands[1] == "files" or commands[1] == "names":
                        save(commands[2], files, variables)
                    elif commands[1] == "added":
                        save(commands[2], added_files, variables)
                    elif commands[1] == "occurances":
                        temp = []
                        temp = [row[0] for row in find_occurances]
                        save(commands[2], temp, variables)
                    else:
                        print(Fore.RED + "Wrong input")
                else:
                    print(Fore.RED + "Wrong input")
                
            elif commands[0] == "load" and commands[1] == "from" and command[3] == "to" and len(commands) == 5:
                if commands[2] in variables:
                    if commands[4] == "files":
                        files = variables[commands[2]].copy()
                        print("Files loaded from \"" + commands[2] + "\"")
                    else:
                        added_files = variables[commands[2]].copy()
                        print("Files loaded from \"" + commands[2] + "\"")
                else:
                    print("File not found")
                        
            elif "input" in commands:
                if len(commands) == 1:
                    input_files(added_files)
                elif len(commands) == 2:
                    input_files(added_files, commands[1])
            
            # output [file] [extend]
            # output "occurances" [file]
            elif "output" in commands:
                if commands[0] == "output" and len(commands) == 1:
                    help_output()
                    return
                
                if commands[1] in variables:
                    output(added_files=variables[commands[1]], output_file="output.txt", extend=False)
                elif commands[1] == "result":
                    output(added_files=result, output_file=commands[2], extend=False)
                elif (commands[1] == "occ" or commands[1] == "occurances") and len(commands) == 2:
                    output_occurances(find_occurances)
                elif (commands[1] == "occ" or commands[1] == "occurances") and len(commands) == 3:
                    output_occurances(find_occurances, commands[2])
                else:
                    extend_choice = True if "extend" in commands else False
                        
                    if 2 <= len(commands) <= 3 :
                        output(added_files=added_files, output_file=commands[1], extend=extend_choice)
                
            elif "names" in commands:
                if len(commands) == 1:
                    pprint(variables)
                elif len(commands) == 2:
                    try:
                        if len(files) == 0:
                            raise Exception("No files to save")
                        names = []
                        for x in files:
                            names.append(x.split("\\")[-1])
                        variables[commands[1]] = names
                        
                        print(f"Names saved to \"{commands[1]}\"")
                    except Exception as e:
                        print(Fore.RED + "Error during saving names: ", e)
            
            elif "history" in commands and len(commands) == 1:
                print_history()
                
            elif "history" in commands and len(commands) == 2:
                r = load_history(int(commands[1]), files, find_occurances)
                if r == 0:
                    print("History loaded successfully")
                else:
                    print("History error occured")
                    
            elif command in ("occ to files", "occ to added", "occurances to files", "occurances to added"):
                try:
                    files.clear()
                    files.extend([x[0] for x in find_occurances])
                    print("Occurances to files successful")
                    add_history(command, files, find_occurances)
                except:
                    print("Error during conversion occurances to files")

                
            # Sjednocení, průnik, rozdíl
            elif "A" in commands or "U" in commands or "-" in commands:
                temp = set_operations(command, variables)
                files.clear()
                files.extend(temp)
                add_history(command, files)
                
            elif command.startswith("load"):    
                parenthesses = command[command.index("(") + 1:command.index(")")]
                if parenthesses == "added" or parenthesses == "added_files":
                    return load(added_files)            
                else:
                    return load(command[command.index("(") + 1:command.index(")")])
                
            
            elif command.startswith("\"") and command.endswith("\""):
                return command[1:-1]
            
            elif command.isdecimal():
                try:
                    return float(command)
                except:
                    return int(command)
            
            elif command == "variables":
                for x in variables:
                    if isinstance(variables[x], list):
                        print(f"{x}:")
                        for y in variables[x]:
                            print("\t" + y)
                    else:
                        print(f"{x}: {variables[x]}")
            
            else:
                command_to_run = convert_variables_to_variables_from_dict(command, variables)
                return execute_command(command_to_run, variables)