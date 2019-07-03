import struct
import re
def LZ77_search(search, look_ahead):

	 ls = len(search)
	 llh = len(look_ahead)
 
	 if(ls==0):
	 	return (0,0, look_ahead[0])
	 
	 if(llh)==0:
	 	return (-1,-1,"")

	 best_length=0
	 best_offset=0 
	 buf = search + look_ahead

	 search_pointer = ls	
	 for i in range(0,llh):
	 	length = 0
	 	if search.find(look_ahead[0:llh - i])!=-1:
	 		ind = [m.start() for m in re.finditer(look_ahead[0:llh - i],search)]
	 		finp = 0
	 		loop = len(look_ahead[0:llh - i]) 
	 		while look_ahead[finp]==look_ahead[loop]:
	 			finp+=1
	 			loop+=1
	 			length+=1
	 			if finp + 1>len(look_ahead[0:llh - i]):
	 				finp=0
	 		best_offset = len(search) - ind[-1]
	 		best_length = length + len(look_ahead[0:llh - i])
	 		break

	 return (best_offset, best_length, buf[search_pointer+best_length])



def main():
	
	x = 16
	MAXSEARCH = 7
	MAXLH =  6

	input = parse("TBC.txt")
	#file_to_read = sys.argv[1] 
	file = open("compressed.zip", "wb")
	searchit = 0;
	lhit = 0;

	while lhit<len(input):
		search = input[searchit:lhit]
		look_ahead = input[lhit:lhit+MAXLH]
		(offset, length, char) = LZ77_search(search, look_ahead)
		#print (offset, length, char)
		
		#print(search)
		
		shifted_offset = offset << 6
		offset_and_length = shifted_offset+length 
		ol_bytes = struct.pack(">Hc",offset_and_length,char)  
		file.write(ol_bytes) 
		 

		lhit = lhit + length + 1
		searchit = lhit - MAXSEARCH

		if searchit<0:
			searchit=0
		 	

	file.close()
		 

def parse(file):
	r=[]
	f = open(file, "rb" )
	text = f.read()
	return text

if __name__== "__main__":
	main()
