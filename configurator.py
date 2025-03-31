import argparse
import multiprocessing
import os
import sys
import threading
import time

from colorama import Fore, init
from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout

import python.global_variables as global_variables
from python.decider import process_command
from python.help_func import (comments_removal, debug_write,
                              read_commands_from_file, read_json)


def main(args):
    os.system('cls')
    files = []
    added_files = []
    variables = {}  
    
    lock = threading.Lock()
    
    init(autoreset=True)
    
    print(Fore.YELLOW + "Type '?' for help" + Fore.RESET)
            
    readed_commands = read_commands_from_file()
    typed_commands = []
    commands_to_process = readed_commands.copy()
    current_command = ""
    finished_commands = []
    
    def status_check():
        while True:
            if len(commands_to_process) == 0:
                print(Fore.LIGHTBLUE_EX + f"{global_variables.path}" + Fore.GREEN + f" >> " + Fore.RESET, end="")
            # else:
            #     print(Fore.LIGHTBLUE_EX + f"{global_variables.path}" + Fore.GREEN + f" >> " + Fore.RESET + commands_to_process[0])
                
            time.sleep(0.2)
            cmd = input()
            sys.stdout.write("\033[F")  # Posune kurzor o řádek zpět
            sys.stdout.write("\033[K")  # Vymaže celý řádek
            if cmd == "status":
                with lock:
                    print(f"Processed commands: {len(finished_commands)} / {len(readed_commands) + len(typed_commands)}", flush=True)
                    print(f"Past commands: ", flush=True)
                    for x in finished_commands:
                        print("\t" + x)
                    if current_command != "":
                        print(f"Current command: \n\t{current_command}")
                        if global_variables.status != "":
                            print(f"\tStatus: {global_variables.status}")
                    print(f"Upcoming commands: ", flush=True)
                    for x in commands_to_process:
                        print("\t" + x)
            elif cmd == "exit":
                break
            else:
                commands_to_process.append(cmd)
                typed_commands.append(cmd)
            
    threading.Thread(target=status_check, daemon=True).start()
    while True:
        if len(commands_to_process) > 0:
            command = commands_to_process.pop(0)
            with lock:
                current_command = command
            
            command = comments_removal(command)
            
            print(Fore.LIGHTBLUE_EX + f"{global_variables.path}" + Fore.GREEN + f" >> " + Fore.RESET + command)
            
            command_start_time = time.time()
            
            if(process_command(command, variables, files, added_files)) == -1:
                return -1

            debug_write(f'Command "{command}" took {time.time() - command_start_time:.4f} seconds to run')
            
            with lock:
                finished_commands.append(command)
                current_command = ""
                
            if len(commands_to_process) == 0:
                print(Fore.LIGHTBLUE_EX + f"{global_variables.path}" + Fore.GREEN + f" >> " + Fore.RESET, end="")
                
        else:
            time.sleep(0.2)
        

if __name__ == "__main__":
    init(autoreset=True)
    multiprocessing.freeze_support()
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('-p', type=str, default="", help='Path to the folder')
    
    if os.path.isfile("debug.txt"):
        os.remove("debug.txt")
        
    if os.path.isfile("output/output.txt"):
        os.remove("output/output.txt")
    
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

    
    # cProfile.run("main(args)", sort="tottime")
    main(args)
    
    print(f"Program took {time.time() - start_time:.4f} seconds to run")
