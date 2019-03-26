#!/usr/bin/python3
from timeit import timeit


print(timeit('''
import os
os.system("./main_beta.py --add Fix.You-Coldplay")
''', number=1), "s execution time!", sep='')
