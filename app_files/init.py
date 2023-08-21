# Initialising by installing all required dependencies
import torch
import subprocess
import os

# path to the working directory

def init():
    torch.set_default_dtype(torch.float32)
    PATH_DIR = os.getcwd()
    path = os.path.join(PATH_DIR, 'config.txt')
    
    with open(path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        print(line)
        ret_code = subprocess.call(['pip', 'install', line])
        if ret_code != 0:
           print(line, 'install unsucessful')
           exit()

    print('Initialisation successful!')

init()


