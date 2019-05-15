#############################
######## Input File #########
#############################
import os

def input_file():
    print("Enter full path of file to compress: ")
    file = input()

    try:
        f = open(file)
        lines = f.readlines()
        for line in lines:
           words = line.strip().split(' ')
           print(words)

        f.close()
    except FileNotFoundError:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("File not found... Try again")
        input_file()

input_file()