#############################
######## Lempel Ziv #########
#############################

import sys
from sys import argv
from struct import *

def compress():
    input_file = input("Input file: ")
    n = input("No. of bytes: ")
    maximum_table_size = pow(2,int(n))      
    file = open(input_file)                 
    data = file.read()  
    # Building and initializing the dictionary.
    dictionary_size = 256                   
    dictionary = {chr(i): i for i in range(dictionary_size)}    
    string = ""             # String is null.
    compressed_data = []    # variable to store the compressed data.

    # iterating through the input symbols.
    # LZW Compression algorithm
    for symbol in data:                     
        string_plus_symbol = string + symbol # get input symbol.
        if string_plus_symbol in dictionary: 
            string = string_plus_symbol
        else:
            compressed_data.append(dictionary[string])
            if(len(dictionary) <= maximum_table_size):
                dictionary[string_plus_symbol] = dictionary_size
                dictionary_size += 1
            string = symbol

    if string in dictionary:
        compressed_data.append(dictionary[string])

    # storing the compressed string into a file (byte-wise).
    out = input_file.split(".")[0]
    output_file = open(out + ".lzw", "wb")
    for data in compressed_data:
        output_file.write(pack('>H',int(data)))
        
    output_file.close()
    file.close()

def decompress():
    input_file = input("Input file: ")
    n = input("No. of bytes: ")
    maximum_table_size = pow(2,int(n))
    file = open(input_file, "rb")
    compressed_data = []
    next_code = 256
    decompressed_data = ""
    string = ""

    # Reading the compressed file.
    while True:
        rec = file.read(2)
        if len(rec) != 2:
            break
        (data, ) = unpack('>H', rec)
        compressed_data.append(data)

    # Building and initializing the dictionary.
    dictionary_size = 256
    dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])

    # iterating through the codes.
    # LZW Decompression algorithm
    for code in compressed_data:
        if not (code in dictionary):
            dictionary[code] = string + (string[0])
        decompressed_data += dictionary[code]
        if not(len(string) == 0):
            dictionary[next_code] = string + (dictionary[code][0])
            next_code += 1
        string = dictionary[code]

    # storing the decompressed string into a file.
    out = input_file.split(".")[0]
    output_file = open(out + "_decoded.txt", "w")
    for data in decompressed_data:
        output_file.write(data)
        
    output_file.close()
    file.close()

def modified_compress(data):

    x = data.decode("utf-8", errors="ignore")

    n = 1000
    maximum_table_size = pow(2,int(n))    
    # Building and initializing the dictionary.
    dictionary_size = 256                 
    dictionary = {chr(i): i for i in range(dictionary_size)}    
    string = ""             # String is null.
    compressed_data = []    # variable to store the compressed data.

    # iterating through the input symbols.
    # LZW Compression algorithm
    for symbol in x:
        string_plus_symbol = string + symbol # get input symbol.
        
        if string_plus_symbol in dictionary: 
            string = string_plus_symbol
        else:
            compressed_data.append(dictionary[string])
            if(len(dictionary) <= maximum_table_size):
                dictionary[string_plus_symbol] = dictionary_size
                dictionary_size += 1
            string = str(symbol)
       
    if string in dictionary:
        compressed_data.append(dictionary[string])

    # storing the compressed string into a file (byte-wise).
    input_file = "a.txt"
    out = input_file.split(".")[0]
    output_file = open(out + ".lzw", "wb")
    for data in compressed_data:
        output_file.write(pack('>H',int(data)))
        
    output_file.close()

def modified_decompress():

    input_file = "a.lzw"
    n = 1000
    maximum_table_size = pow(2,int(n))
    file = open(input_file, "rb")
    compressed_data = []
    next_code = 256
    decompressed_data = ""
    string = ""

    # Reading the compressed file.
    while True:
        rec = file.read(2)
        if len(rec) != 2:
            break
        (data, ) = unpack('>H', rec)
        compressed_data.append(data)

    # Building and initializing the dictionary.
    dictionary_size = 256
    dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])

    # iterating through the codes.
    # LZW Decompression algorithm
    for code in compressed_data:
        if not (code in dictionary):
            dictionary[code] = string + (string[0])
        decompressed_data += dictionary[code]
        if not(len(string) == 0):
            dictionary[next_code] = string + (dictionary[code][0])
            next_code += 1
        string = dictionary[code]

    output_file = open("am_decoded.txt", "wb")
    
    s = ""
    for data in decompressed_data:
        s = s + data

    x = s.encode()

    b = bytearray()
    for i in x:
        b.append(i)
    print(b)
    output_file.write(bytes(b))

    file.close()
    output_file.close()

    return x
