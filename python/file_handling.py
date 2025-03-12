import os

from colorama import Fore

from python.MyFile import Molecule, MyFile


def load(name):
    if isinstance(name, list):
        files = []
        for file in name:
            files.append(load(file))
                
        return files
    
    if name.endswith(".bnx"):
        return load_bnx(name)
    elif name.endswith(".cmap"):
        return load_cmap(name)
    elif name.endswith(".xmap"):
        return load_xmap(name)
        
def load_bnx(name):
    if os.path.isfile(name):
        with open(name, 'r') as f:
            my_f = MyFile()
            
            my_f.name = name
            my_f.size = os.path.getsize(name)
            my_f.content = f.read()
            lines = my_f.content.split("\n")
            
            for line in lines:
                if line == "":
                    continue
                
                if line[0] == "#" and "h" in line:
                    first_word = line.split()[0]
                    header_id = first_word[1:first_word.find("h")]
                    
                    if header_id.isdecimal() or header_id == "Q":                        
                        header = line.split()[1:]
                        header.insert(0, header_id)
                        
                        my_f.header.append(header)
                    
                if not line.startswith("#"):
                    molecule = Molecule()
                    
                    data = line.strip().split("\t")
                        
                    headers = my_f.header  
                    for i, header in enumerate(headers):
                        if isinstance(header, list) and len(header) - 1 == len(data) and data[0] == header[0]:
                            for h, d in zip(header[1:], data):
                                setattr(molecule, h, d)
                            break
                        elif data[0] == header[0]:
                            for i, h in enumerate(header[1:]):
                                if "[N]" in h:
                                    molecule.__setattr__(h, data[i:])
                                else:
                                    molecule.__setattr__(h, data[i])
                            break
                        elif data[0][0] == header[0]:
                            for i, h in enumerate(header[1:]):
                                if "[N]" in h:
                                    molecule.__setattr__(h, data[i:])
                                else:
                                    molecule.__setattr__(h, data[i])

                    
                    if molecule._specs:
                        my_f.add_molecule(molecule)
            
            
            return my_f
    else:
        print(Fore.RED + "load error")
        
def load_cmap(name):
    if os.path.isfile(name):
        with open(name, 'r') as f:
            my_f = MyFile()
            
            my_f.name = name
            my_f.size = os.path.getsize(name)
            my_f.content = f.read()
            lines = my_f.content.split("\n")
            
            for line in lines:
                if line == "":
                    continue
                if line.startswith("#h"):
                    my_f.header = line.removeprefix("#h").strip().split("\t")
                    
                if not line.startswith("#"):
                    molecule = Molecule()
                    
                    data = line.strip().split("\t")
                        
                    headers = my_f.header  
                    for i, header in enumerate(headers):
                        if isinstance(header, list):
                            if len(header) == len(data):
                                for j, h in enumerate(header):
                                    molecule.__setattr__(h, data[j])
                        else:
                            molecule.__setattr__(header, data[i])
                    
                    my_f.molecules.append(molecule)
            
            
            return my_f
    else:
        print(Fore.RED + "load error")
        
def load_xmap(name):
    if os.path.isfile(name):
        with open(name, 'r') as f:
            my_f = MyFile()
            
            my_f.name = name
            my_f.size = os.path.getsize(name)
            my_f.content = f.read()
            lines = my_f.content.split("\n")
            
            for line in lines:
                if line == "":
                    continue
                if line.startswith("#h"):
                    my_f.header = line.removeprefix("#h").strip().split("\t")
                    
                if not line.startswith("#"):
                    molecule = Molecule()
                    
                    data = line.strip().split("\t")
                        
                    headers = my_f.header  
                    for i, header in enumerate(headers):
                        if isinstance(header, list):
                            if len(header) == len(data):
                                for j, h in enumerate(header):
                                    molecule.__setattr__(h, data[j])
                        else:
                            molecule.__setattr__(header, data[i])
                    
                    my_f.molecules.append(molecule)
            
            
            return my_f
    else:
        print(Fore.RED + "load error")