import random
import time
from time import sleep

from python.parallel_for import _shared_globals


def return_list(l : list, shared_data=None, worker_id=None):
    sleep(random.uniform(0, 1))
    
    print(f"Worker {worker_id} sees path: {_shared_globals['path']}")
    
    test = 0
    
    for x in l:
        test = x
        
    
    print("Returning list...")
    return l

def average_snr(file, shared_data=None, worker_id=None):
    data = file["data"]
    
    total_snr = 0
    num_of_molecules = 0
    
    for molecule in data:
        if "SNR" in molecule:
            total_snr += molecule["SNR"]
            num_of_molecules += 1
            

    # Simulace narocne operace / velkeho souboru
    # time.sleep(5)

    return (file["filename"], total_snr / num_of_molecules)