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

class My_file:
    def __init__(self):
        self.name = ""
        self.size = -1
        self.header = []
        self.content = ""
        self.molecules = []
        
    def __str__(self):
        return (f"\nname: {self.name}\nheader: {self.header}\ncontent: {repr(self.content[:100])}..."
            f"\nsize: {self.size} bytes\nnumber of molecules: {len(self.molecules)}\n")
    
    def __repr__(self):
        return (f"\nname: {self.name}\nheader: {self.header}\ncontent: {repr(self.content[:100])}..."
            f"\nsize: {self.size} bytes\nnumber of molecules: {len(self.molecules)}\n")