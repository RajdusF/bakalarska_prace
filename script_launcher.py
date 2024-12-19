import os
import shutil
import subprocess
from time import sleep

from colorama import Fore
from tqdm import tqdm


def convert_to_wsl_path(windows_path):
    wsl_path = windows_path.replace("\\", "/")
    if wsl_path[1:3] == ":/":
        wsl_path = "/mnt/" + wsl_path[0].lower() + wsl_path[2:]
    return wsl_path

def read_scripts_to_run():
    readed_scripts = []
    f = open("C:\\Users\\Filip\\Documents\\bakalarska_prace\\scripts_to_run.txt", "r")
    for line in f:
        if not line.startswith('#'):
            s = line.strip()
            readed_scripts.append(s)
        
    f.close()      
    
    return readed_scripts

def load_scripts_from_script_folder(readed_scripts):
    scripts = []
    script_folder = "C:\\Users\\Filip\\Documents\\bakalarska_prace\\scripts"
    
    if readed_scripts == []:
        for file in os.listdir(script_folder):
            if file.endswith(".sh"):
                scripts.append(file)
        return scripts
    else:
        for readed_script in readed_scripts:
            if not os.path.exists(script_folder + "\\" + readed_script.split(" ")[0]):
                continue
            scripts.append(readed_script)
            
    return scripts

files = []
readed_scripts = read_scripts_to_run()
scripts = load_scripts_from_script_folder(readed_scripts)

# Load files to copy
f = open("C:\\Users\\Filip\\Documents\\bakalarska_prace\\output.txt", "r")
for line in f:
    if os.path.exists(line.strip()):
        s = line.strip()
        files.append(s)
    
f.close()

print("Loaded files:")
for file in files:
    print(f"\t{file.split('\\')[-1]}")
print("Loaded scripts to run in order:")
for script in scripts:
        print(f"\t{script}")
    
print("Press any key to continue...")
input()

if not os.path.exists("./output"):
    os.makedirs("./output")


total_iterations = len(files) + len(scripts) * len(files)


with tqdm(total=total_iterations, desc="Total Progress", position=0, leave=True) as pbar:
    for file in files:
        try:
            destination = "./output/" + file.split("\\")[-1]
            shutil.copy(file, destination)
            if len(file) > 40:
                file = "..." + file[-40:]
            if len(destination) > 40:
                destination = "..." + destination[-40:]
            tqdm.write(Fore.LIGHTGREEN_EX + f"File copied from {file} to {destination}" + Fore.RESET)
        except FileNotFoundError:
            tqdm.write(Fore.LIGHTRED_EX + f"Source file {file} not found." + Fore.RESET)
        except PermissionError:
            tqdm.write(Fore.LIGHTRED_EX + "Permission denied." + Fore.RESET)
        except Exception as e:
            tqdm.write(Fore.LIGHTRED_EX + f"An error occurred: {e}" + Fore.RESET)
        
        pbar.update(1)
        sleep(0.15)
        
    tqdm.write("\n")


    files.clear()
    files = [os.path.abspath(os.path.join("./output", file)) for file in os.listdir("./output")]

    files = [convert_to_wsl_path(file) for file in files]

    for file in files:
        for script in scripts:
            try:
                words = script.split(" ")
                script_name = words[0]
                command = ["bash", "./scripts/" + script_name, file]

                while len(words) > 1:
                    command.append(words.pop(1))
                
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    check=True
                )
                tqdm.write(Fore.LIGHTGREEN_EX + f"Script '{script}' on file '{file.split("/")[-1]}' successfully started!" + Fore.RESET)
                tqdm.write("Script output:")
                tqdm.write(result.stdout)
            except subprocess.CalledProcessError as e:
                tqdm.write(Fore.LIGHTRED_EX + f"Error while running script '{script}':" + Fore.RESET)
                tqdm.write(e.stderr)
            finally:
                pbar.update(1)
            sleep(0.15)