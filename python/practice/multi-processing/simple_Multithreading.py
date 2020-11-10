import threading
import random


def splitter(words):
    my_list = words.split()
    new_list = []
    while my_list:
        new_list.append(my_list.pop(random.randrange(0, len(my_list))))
    print(' '.join(new_list), '\n')

if __name__ == '__main__':
    sentence = 'I am a different normal happy guy. Word.'
    num_of_threads = 5
    thread_list = []
    
    print('STARTING ... \n')
    for i in range(num_of_threads):
        t = threading.Thread(target=splitter, args=(sentence,))  # target function and tuple as an input
        t.start()
        thread_list.append(t)
        
    print('\nThread Count : {}'.format(threading.activeCount()))
    print('EXITING ... \n')

