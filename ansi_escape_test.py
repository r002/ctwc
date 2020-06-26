# Thursday - June 25, 2020
# Note: Only works in Windows Terminal! (Not PowerShell.)
#       Should also work in Unix!

import time
import sys
import numpy as np

# for i in range(5):
#     print(i, end=' ')
#     sys.stdout.flush()
#     time.sleep(1)


# for i in range(100):
#     # print(i)
#     print(f"{i}\n\r{i}", end="\r")
#     time.sleep(0.5)

def delete_last_line():
    "Use this function to delete the last line in the STDOUT"
    #cursor up one line
    sys.stdout.write('\x1b[1A')
    #delete last line
    sys.stdout.write('\x1b[2K')
    sys.stdout.flush()


def del_twenty_lines():
    sys.stdout.write('\x1b[1A'*20)
    # sys.stdout.write('\x1b[2K')
    sys.stdout.flush()


# print("hello")
# print("hello2")
# print("this line will be delete after 2 seconds")
# time.sleep(2)
# delete_last_line()
# time.sleep(2)
# delete_last_line()

d = np.zeros((20,10))
print(d)
time.sleep(2)
del_twenty_lines()
