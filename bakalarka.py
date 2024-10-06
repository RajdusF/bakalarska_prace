import os

from colorama import Back, Fore, Style, init

init() # inizialization of colorama
 
# path="C:\\Users\\Filip\\Downloads"
path="C:\\Users\\Filip\\Documents\\bakalarka"

for file in os.listdir(path):
    print(file)
    

def compare(file, find):
    index_file = 0
    index_find = 0
    any = False
    
    file = file.lower()
    find = find.lower()
    
    # print("file: " + file + "  " + str(len(file)))
    # print("find: " + find + "  " + str(len(find)))
    length = len(file) if len(file) > len(find) else len(find)
    # print("length:" + str(length))
        
    if "*" not in find and "_" not in find and file == find:
        return True
    if "*" not in find and "_" not in find and file != find:
        return False
    
    if file == find:
        return True
    
    for _ in range(length):
        if index_file == len(file):
            break
        if index_find == len(find):
            break
        elif any == True:
            if find[index_find] == file[index_file]:
                index_file += 1
                index_find += 1
                any = False
            else:
                index_file += 1
        elif find[index_find] == "*":
            any = True
            index_file += 1
            index_find += 1
        elif find[index_find] == "_":
            index_file += 1
            index_find += 1
        elif find[index_find] != file[index_file]:
            return False
        elif find[index_find] == file[index_file]:
            index_file += 1
            index_find += 1

    if index_find == len(find) and index_file == len(file):
        return True
    else:
        return False

while True:
    find = input(Fore.GREEN + "##########################################\nfind: ")
    print("##########################################" + Fore.RESET)
    for file in os.listdir(path):
        if compare(file, find):
            print(file)