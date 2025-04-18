import random
from time import sleep

from python.parallel_for import _shared_globals


def show_length(l:dict, shared_data=None, worker_id=None):
    
    r = []
    
    data = l["data"]
    
    print(f"len(data) = {len(data)}")
    
    # print(data[1])
    
    for x in data:
        if dict(x).get("Length") != None and x["Length"] > 1_000_000:
            r.append(x)        
            
    return r
    

def count_to(num, display=True):
    """Counts to a given number."""
    
    print(f"Counting to {num}...")
    
    for i in range(1, num + 1):
        if display:
            print(i)

    print("Done counting!")
    
    
def find_44(l : list):
    for x in l:
        if x == 440_00000:
            print("Found 44!")
            
    print("Done searching!")
    return None

def return_list(l : list, shared_data=None, worker_id=None):
    sleep(random.uniform(0, 1))
    
    print(f"Worker {worker_id} sees path: {_shared_globals['path']}")
    
    test = 0
    
    for x in l:
        test = x
        
    
    print("Returning list...")
    return l