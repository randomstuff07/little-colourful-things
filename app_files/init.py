# Initialising by installing all required dependencies

import subprocess
import os
import sys
import pkg_resources
# path to the working directory

def init(PATH_DIR):
    path = os.path.join(PATH_DIR, 'config.txt')
    
    with open(path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        print(line)
        ret_code = subprocess.call(['pip', 'install', line])
        if ret_code != 0:
           print(line, ' install unsucessful')
           exit

    print('Initialisation successful!')


