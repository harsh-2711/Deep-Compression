#############################
###### Huffman Coding #######
#############################

import heapq
import os
from functools import total_ordering

import sys
from sys import argv
from struct import *

class HeapNode:
	def __init__(self, char, freq):
		self.char = char
		self.freq = freq
		self.left = None
		self.right = None

	# defining comparators less_than and equals
	def __lt__(self, other):
		return self.freq < other.freq

	def __eq__(self, other):
		if(other == None):
			return False
		if(not isinstance(other, HeapNode)):
			return False
		return self.freq == other.freq


class HuffmanCoding:
	def __init__(self, path):
		self.path = path
		self.heap = []
		self.codes = {}
		self.reverse_mapping = {}

	# functions for compression:

	def make_frequency_dict(self, text):
		frequency = {}
		for character in text:
			if not character in frequency:
				frequency[character] = 0
			frequency[character] += 1
		return frequency

	def make_heap(self, frequency):
		for key in frequency:
			node = HeapNode(key, frequency[key])
			heapq.heappush(self.heap, node)

	def merge_nodes(self):
		while(len(self.heap)>1):
			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			merged = HeapNode(None, node1.freq + node2.freq)
			merged.left = node1
			merged.right = node2

			heapq.heappush(self.heap, merged)

	def make_codes_helper(self, root, current_code):
		if(root == None):
			return

		if(root.char != None):
			self.codes[root.char] = current_code
			self.reverse_mapping[current_code] = root.char
			return

		self.make_codes_helper(root.left, current_code + "0")
		self.make_codes_helper(root.right, current_code + "1")

	def make_codes(self):
		root = heapq.heappop(self.heap)
		current_code = ""
		self.make_codes_helper(root, current_code)

	def get_encoded_text(self, text):
		encoded_text = ""
		for character in text:
			encoded_text += self.codes[character]
		return encoded_text

	def pad_encoded_text(self, encoded_text):
		extra_padding = 8 - len(encoded_text) % 8
		for i in range(extra_padding):
			encoded_text += "0"

		padded_info = "{0:08b}".format(extra_padding)
		encoded_text = padded_info + encoded_text
		return encoded_text

	def get_byte_array(self, padded_encoded_text):
		if(len(padded_encoded_text) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		b = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
			byte = padded_encoded_text[i:i+8]
			b.append(int(byte, 2))
		return b

	def compress(self):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + "_compressed.txt"

		with open(self.path, 'r+') as file:
			text = file.read()
			text = text.rstrip()

			frequency = self.make_frequency_dict(text)
			self.make_heap(frequency)
			self.merge_nodes()
			self.make_codes()

			encoded_text = self.get_encoded_text(text)
			
			self.modified_compress(encoded_text)

		print("Compressed")
		return output_path


	""" functions for decompression: """

	def remove_padding(self, padded_encoded_text):
		padded_info = padded_encoded_text[:8]
		extra_padding = int(padded_info, 2)

		padded_encoded_text = padded_encoded_text[8:] 
		encoded_text = padded_encoded_text[:-1*extra_padding]

		return encoded_text

	def decode_text(self, encoded_text):
		current_code = ""
		decoded_text = ""

		for bit in encoded_text:
			current_code += bit
			if(current_code in self.reverse_mapping):
				character = self.reverse_mapping[current_code]
				decoded_text += character
				current_code = ""

		return decoded_text

	def decompress(self, input_path):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + "_decompressed" + ".txt"

		with open(input_path, 'rb') as file, open(output_path, 'w') as output:
			bit_string = ""

			byte = file.read(1)
			while(len(byte) > 0):
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')
				bit_string += bits
				byte = file.read(1)

			xyz = LempelZiv.modified_decompress()

			encoded_text = self.remove_padding(bit_string)

			decompressed_text = self.decode_text(encoded_text)

			output.write(decompressed_text)

		print("Decompressed")
		return output_path

	#############################
	######## Lempel Ziv #########
	#############################


	def modified_compress(self,get_data):

	    n = 1000
	    maximum_table_size = pow(2,int(n))
	    # Building and initializing the dictionary.
	    dictionary_size = 256                 
	    dictionary = []  
	    string = ""             # String is null.
	    compressed_data = []    # variable to store the compressed data.

	    # iterating through the input symbols.
	    # LZW Compression algorithm
	    for symbol in get_data:
	    	string_plus_symbol = string + symbol # get input symbol  
	    	if string_plus_symbol in dictionary: 
	    		string = string_plus_symbol
	    	else:
	            compressed_data.append(string)
	            dictionary.append(string_plus_symbol)
	            string = str(symbol)
	       
	    if string in dictionary:
	        compressed_data.append(string)

	    # storing the compressed string into a file (byte-wise).
	    input_file = "a.txt"
	    out = input_file.split(".")[0]
	    output_file = open(out + ".lzw", "w")
	    for data in compressed_data:
	        output_file.write(data)
	        
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


h = HuffmanCoding("a.txt")
h.compress()