from multiprocessing import Pool


def start_function_for_processes(n):
    result_sent_back_to_parent = n * n
    return result_sent_back_to_parent


if __name__ == "__main__":
    
    with Pool(processes=5) as p:
        
        results = p.map(start_function_for_processes, range(2000), chunksize=10)
    
    print(results)