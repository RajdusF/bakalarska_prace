import inspect
import multiprocessing
from functools import partial
from itertools import count
from typing import Any, Callable, List, Optional

import numpy as np
from colorama import Fore

import python.global_variables as global_variables

_shared_globals = None


def init_worker(shared_data):
    global _shared_globals
    _shared_globals = shared_data

def worker_wrapper(func, args_tuple, shared_data, chunk_with_id):
    chunk_id, chunk = chunk_with_id
    
    try:
        func.__globals__["_shared_globals"] = _shared_globals
        return func(chunk, *args_tuple, shared_data=shared_data, worker_id=chunk_id)
    except Exception as e:
        print(Fore.RED + f"Worker wrapper {chunk_id} error: {e}" + Fore.RESET)
        return []

def pfor_order(func, items, *args, num_cores=None):
    if not items:
        return []
    
    items = [items] if isinstance(items, str) else list(items)
    num_cores = num_cores or multiprocessing.cpu_count()
    num_cores = min(num_cores, len(items))
    
    chunks = np.array_split(items, num_cores)
    chunks_with_ids = [(i, list(chunk)) for i, chunk in enumerate(chunks) if len(chunk) > 0]
    
    shared_data = {
        'path': getattr(global_variables, 'path', ''),
        'variables': getattr(global_variables, 'variables', {})
    }

    print(f"{Fore.YELLOW}Starting {num_cores} cores...{Fore.RESET}")
    
    with multiprocessing.Pool(num_cores, initializer=init_worker, initargs=(shared_data,)) as pool:
        try:
            worker_partial = partial(
                worker_wrapper,
                func,
                args,
                shared_data
            )
            
            results = pool.map(worker_partial, chunks_with_ids)
            
            return [item for sublist in results if sublist for item in (sublist if isinstance(sublist, list) else [sublist])]
        
        finally:
            pool.close()
            pool.join()


def pfor(func, items, *args, num_cores=None):
    if not items:
        return []
    
    items = [items] if isinstance(items, str) else list(items)
    num_cores = num_cores or multiprocessing.cpu_count()
    num_cores = min(num_cores, len(items))
    
    chunks = np.array_split(items, num_cores)
    chunks_with_ids = [(i, list(chunk)) for i, chunk in enumerate(chunks) if len(chunk) > 0]
    
    shared_data = {
        'path': getattr(global_variables, 'path', ''),
        'variables': getattr(global_variables, 'variables', {})
    }
    
    print(f"{Fore.YELLOW}Starting {num_cores} cores...{Fore.RESET}")
    

    with multiprocessing.Pool(num_cores) as pool:
        try:
            worker_partial = partial(
                worker_wrapper,
                func,
                args,
                shared_data
            )
            
            results = []
            for result in pool.imap_unordered(worker_partial, chunks_with_ids):
                if result:
                    results.extend(result if isinstance(result, list) else [result])
            return results
            
        finally:
            pool.close()
            pool.join()
            
            
def has_argument(func, arg_name):
    signature = inspect.signature(func)
    for param in signature.parameters.values():
        if param.name == arg_name:
            return True
    return False