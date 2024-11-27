import os

from colorama import Fore

import global_variables
from command_functions import (add, add_folder, input_files, output, remove,
                               save, select, set_operations, settings,
                               show_files, sort)
from help_func import (add_history, help_add, help_cd, help_filter,
                       help_output, help_select, help_sort, load_history,
                       my_help, print_history, show_added_files,
                       show_current_folder)


def process_command(command : str, dict, files : list, added_files : list):
    from filter import filter
    
    commands = command.split(" ")
        
    if command == "exit":
        return -1
    
    if command == "?":
        my_help()
        return
    
    if "**" in command:
        print("Wrong input")
        return
    
    if command == "*":
        show_current_folder()
        # for file in os.listdir(global_variables.path):
        #     print(file)
            
    elif command == "cd.." or command == "cd ..":
        global_variables.path = os.path.abspath(os.path.join(global_variables.path, os.pardir))
        print(f"Current path: {global_variables.path}")
        
    elif "cd" in command:
        path_index = commands.index("cd") + 1
        
        if global_variables.path == None:
            global_variables.path = ""
        
        if path_index < len(commands):
            path = commands[path_index]
            if os.path.isdir(path):
                global_variables.path = path
                print(f"Current path: {global_variables.path}")
            elif os.path.isdir(global_variables.path + "\\" + path):
                global_variables.path = global_variables.path + "\\" + path
                print(f"Current path: {global_variables.path}")
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
        
        temp = filter(commands, files, added_files)
        files.clear()
        files.extend(temp)
        
        
        add_history(command, files)
    
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
    
    elif "find" in commands:
        finds = []
        for file in added_files:
            finds.extend(find(commands[commands.index("find") + 1:], file))
            
        print(Fore.GREEN + f"Found {len(finds)} occurances:" + Fore.RESET)
        for find in finds:
            print(find)
    
    elif "add" in commands and len(commands) > 1:
        if commands[0] == "add" and len(commands) == 1:
            help_add()
            return
        
        if commands[1] == "*" and len(commands) == 2:
            add("*", files, added_files)
        elif "\\" in command and len(commands) == 2:
            added_files.extend(add_folder(commands[1]))
        elif "\\" in command and len(commands) == 3 and "all" in commands:
            added_files.extend(add_folder(commands[2], recursive=True))
            
        elif len(commands) == 2:
                name = commands[1]
                add(name, files, added_files)
        else:
            print("Wrong input")
            return
        
        print(f"Added files ({len(added_files)}):")
        for x in added_files:
            print(x)
            
    elif "remove" in commands:
        r = remove(commands, added_files)
        print(f"Removed {r} files")
            
    elif "show" in commands:
        if len(commands) == 2 and commands[1] == "added":
            show_added_files(added_files)
        elif len(commands) == 2 and commands[1] == "files":
            show_files(files)
        elif len(commands) == 2:                          # dict[commands[1]]):
            if dict.get(commands[1]) != None:
                print(f"Files in \"{commands[1]}\":")
                for x in dict[commands[1]]:
                    print(x)
            else:
                print(f"Save file {commands[4]} not found")
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
        elif len(commands) == 1:
            print(f"Default unit: {global_variables.default_unit}")
            print(f"Search folders: {global_variables.search_folders}")
            print(f"Show duplicity: {global_variables.show_duplicity}")
            return

        
    elif commands[0] == "save" and commands[2] == "to" and len(commands) == 4:
        if commands[1] == "files":
            save(commands[3], files, dict)
        elif commands[1] == "added":
            save(commands[3], added_files, dict)
        else:
            print("Wrong input")
        
    elif commands[0] == "load" and commands[1] == "from" and command[3] == "to" and len(commands) == 5:
        if commands[2] in dict:
            if commands[4] == "files":
                files = dict[commands[2]].copy()
                print("Files loaded from \"" + commands[2] + "\"")
            else:
                added_files = dict[commands[2]].copy()
                print("Files loaded from \"" + commands[2] + "\"")
        else:
            print("File not found")
                
    elif "input" in commands:
        if len(commands) == 1:
            input_files(added_files)
        elif len(commands) == 2:
            input_files(added_files, commands[1])
    
    elif "output" in commands:
        if commands[0] == "output" and len(commands) == 1:
            help_output()
            return
        
        extend_choice = True if "extend" in commands else False
             
        if 2 <= len(commands) <= 3 :
            output(added_files=added_files, output_file=commands[1], extend=extend_choice)
        
    elif "history" in commands and len(commands) == 1:
        print_history()
        
    elif "history" in commands and len(commands) == 2:
        try:
            temp = load_history(int(commands[1]))
            files.clear()
            files.extend(temp)
            show_files(files)
        except:
            print("Wrong input")
            
    elif "ls" in commands and len(commands) == 1:
        show_current_folder()
        
    # Sjednocení, průnik, rozdíl
    elif "A" in commands or "U" in commands or "-" in commands:
        temp = set_operations(command, dict)
        files.clear()
        files.extend(temp)
        add_history(command, files)
        
        
    elif command == "":
        return
    
    else:
        print("Wrong input")