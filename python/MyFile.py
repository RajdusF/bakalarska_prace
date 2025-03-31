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
    
class XData:
    def __init__(self, data=None):
        if data is None:
            self.data = dict()
        else:
            self.data = data
            
    # def __getitem__(self, key):
    #     return self.data[key]
    
    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        
    def __str__(self):
        return str(self.data)
