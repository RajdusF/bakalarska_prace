class Molecule:
    def __init__(self):
        self._specs = {}

    def __getattr__(self, name):
        if name in self._specs:
            return self._specs[name]
        raise AttributeError(f"Attribute '{name}' not found")

    def __setattr__(self, name, value):
        if name == "_specs":
            super().__setattr__(name, value)
        else:
            self._specs[name] = value
            
    def __str__(self):
        text = ""
        for x in self._specs.values():
            text += str(x) + "\t"
        return text

class MyFile:
    def __init__(self):
        self.name = ""
        self.size = -1
        self.header = []
        self.content = ""
        self.molecules = []
        
    def __str__(self):
        header_str = "\n\t\t".join(map(str, self.header)) if isinstance(self.header, list) else self.header
        
        return (f"\tname: {self.name}\n"
                f"\theader: {header_str}\n"
                f"\tcontent: {repr(self.content[:100])}...\n"
                f"\tsize: {self.size} bytes\n"
                f"\tnumber of molecules: {len(self.molecules)}\n")
    
    def __repr__(self):
        return (f"\tname: {self.name}\n\theader: {self.header}\n\tcontent: {repr(self.content[:100])}..."
            f"\n\tsize: {self.size} bytes\n\tnumber of molecules: {len(self.molecules)}\n")
        
    def add_molecule(self, molecule):
        self.molecules.append(molecule)

    def get_molecule(self, index):
        return self.molecules[index]