import argparse
import cProfile
import os
import time

from colorama import Fore, init

import python.global_variables as global_variables
from python.decider import process_command
from python.help_func import debug_write, read_commands_from_file, read_json


def main(args):
    os.system('cls')
    files = []
    added_files = []
    dict = {}    
        
    print(Fore.YELLOW + "Type '?' for help" + Fore.RESET)
            
    commands = read_commands_from_file()
    
    while len(commands) > 0:
        command = commands.pop(0)
        if command.startswith("#"):
            continue
        print(Fore.LIGHTBLUE_EX + f"{global_variables.path}" + Fore.GREEN + f" >> {command}" + Fore.RESET)
        command_start_time = time.time()
        if(process_command(command, dict, files, added_files)) == -1:
            return -1
        print(f'Command "{command}" took {time.time() - command_start_time:.4f} seconds to run')
        debug_write(f'Command "{command}" took {time.time() - command_start_time:.4f} seconds to run')
        
    
    while True:         
        command = input(Fore.LIGHTBLUE_EX + f"{global_variables.path}" + Fore.GREEN + " >> ")
        print(Fore.RESET, end="")
            
        command_start_time = time.time()
        
        result = process_command(command, dict, files, added_files)
        
        print(f'Command "{command}" took {time.time() - command_start_time:.4f} seconds to run')
        debug_write(f'Command "{command}" took {time.time() - command_start_time:.4f} seconds to run')
        
        if result == -1:
            break


if __name__ == "__main__":
    init(autoreset=True)
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('-p', type=str, default="", help='Path to the folder')
    
    if os.path.isfile("debug.txt"):
        os.remove("debug.txt")
    
    args = parser.parse_args()
    
    start_time = time.time()  
    
    read_json("settings.json")
    
    if args.p != "":
        print(f"args.p: {args.p}")
        if os.path.exists(args.p):
            global_variables.path = args.p
        else:
            print(Fore.RED + "Path not found" + Fore.RESET)
        
        
    print(Fore.YELLOW + "Settings:" + Fore.RESET)
    print(f"Default unit: {global_variables.default_unit}")
    print(f"Search folders: {global_variables.search_folders}")
    print(f"Show duplicity: {global_variables.show_duplicity}")

    
    cProfile.run("main(args)", sort="tottime")
    # main(args)
    
    print(f"Program took {time.time() - start_time:.4f} seconds to run")