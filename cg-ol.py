import os
import sys
import time
import random
import termcolor

def init_array(width, height):
    return [[0  for j in range(width)] for i in range(height)]

def random_init_array(width, height):
    return [[random.randint(0, 1) for j in range(width)] for i in range(height)]

def count_c(array, row, col):
    cr = len(array)
    cc = len(array[0])
    ffi = lambda x, y: (y + x) % y
    count = array[ffi(row - 1, cr)][ffi(col - 1, cc)] +\
             array[ffi(row - 1, cr)][ffi(col, cc)] +\
             array[ffi(row - 1, cr)][ffi(col + 1, cc)] +\
             array[ffi(row, cr)][ffi(col - 1, cc)] +\
             array[ffi(row, cr)][ffi(col + 1, cc)] +\
             array[ffi(row + 1, cr)][ffi(col - 1, cc)] +\
             array[ffi(row + 1, cr)][ffi(col, cc)] +\
             array[ffi(row + 1, cr)][ffi(col + 1, cc)]
    return count

def next_state(c_array, rules=[[3], [2, 3]]):
    new_array = []
    for i in range(len(c_array)):
        new_array.append([])
        cursor = len(new_array) - 1
        for j in range(len(c_array[i])):
            if (c_array[i][j] == 0) and (count_c(c_array, i, j) in rules[0]):
                new_array[cursor].append(1)
            elif (c_array[i][j] == 1) and (count_c(c_array,i, j) not in rules[1]):
                new_array[cursor].append(0)
            else:
                new_array[cursor].append(c_array[i][j])
    return new_array

def print_arr(array):
    print("\n".join(["".join([str(j)+"*" for j in i]) for i in c_array]).\
          replace("1*", "\x1b[31mO\x1b[0m").replace("0*", "\x1b[34m.\x1b[0m"))

def edit_arr(row, col):
    if c_array[row][col] == 0:
        c_array[row][col] = 1
    elif c_array[row][col] == 1:
        c_array[row][col] = 1

def test_init_array():
    c_array = init_array(9, 9)
    c_array[5][3] = 1
    c_array[5][4] = 1
    c_array[5][5] = 1
    c_array[4][5] = 1
    c_array[3][4] = 1
    return c_array

def copy_array(array_1, array_2):
    for i in range(len(array_1)):
        if type(array_1[i]) == list:
             array_2.append([])
             for j in range(len(array_1[i])):
                 array_2[len(array_2) - 1].append(array_1[i][j])

def increase_array(array, row, col):
    result = []
    copy_array(array, result)
    addr = row - len(array)
    addc = col - len(array[0])
    down = False
    for i in range(2):
        for j in range(addr // 2):
            if down:
                result.append([0 for i in range(len(array[0]))])
            else:
                result.insert(0, [0 for i in range(len(array[0]))])
        down = True
    if (addr % 2 != 0 and addr > 0):
        result.append([0 for i in range(len(array[0]))])
    right = False
    for i in range(2):
        for j in range(len(result)):
            for j2 in range(addc // 2):
                if right:
                    result[j].append(0)
                else:
                    result[j].insert(0, 0)
        right = True
    if (addc % 2 != 0 and addc > 0):
        for i in range(len(result)):
            result[i].append(0)
    return result

def fconfig(string):
    result = [[j.replace("O", "1").replace(".", "0") for j in i.split()] for i in string.replace(" ", "").split("\n")]
    [result.remove([]) for i in range(result.count([]))]
    return [[int(j3) for j3 in list(j2[0])] for j2 in [[j for j in i] for i in result]]

def fccol(array):
    if (len(array) == 2):
        return [[[int(j) for j in i] for i in array[1].split(":")]]
    elif (len(array) == 3):
        return [array[2], [[int(j) for j in i] for i in array[1].split(":")]]
    return []

if __name__ == "__main__":
    delay = float(input("Input delay: "))
    sp_array = fccol(sys.argv)
    input_conf = ""
    if len(sp_array) < 2:
        print("Input conf.:")
        while True:
            input_string = input()
            if input_string == "":
                break
            input_conf += input_string + "\n"
    elif len(sp_array) == 2:
        file = open(os.path.abspath(sp_array[0]), "r")
        input_conf = file.read()
        file.close()
    if len(sp_array) > 0:
        rules = sp_array[len(sp_array) - 1]
    else:
        rules = [[3], [2, 3]]
    c_array = fconfig(input_conf)
    c_array = increase_array(c_array, 36, 100)
    rows = len(c_array)
    cols = len(c_array[0])
    print("\033[2J", end="")
    print("\033[0;0H", end="")
    print_arr(c_array)
    steps = 0
    while True:
        time.sleep(delay)
        c_array = next_state(c_array, rules)
        steps += 1
        print("\033[2J", end="")
        print("\033[0;0H", end="")
        print_arr(c_array)
        print(f"\nSIZE: {cols}x{rows} DELAY: {delay} STEPS: {steps}")
