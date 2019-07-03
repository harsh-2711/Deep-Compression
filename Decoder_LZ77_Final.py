import struct

def decoder(out, search):
    MAX_SEARCH = search
    file = open("compressed.zip","rb")
    input = file.read()
    
    chararray = ""
    i=0
    
    while i<len(input):
        
        #UNPACKING EVERY 3 BYTES
        (offset_and_length, char)= struct.unpack(">Hc", input[i:i+3])
        
        #FINDING OUT THE LENGTHS
        offset = offset_and_length >> 6
        
        
        length = offset_and_length - (offset<<6)
            
        i=i+3
        
        #case is (0,0,c)
        if(offset == 0) and (length == 0):
            chararray += char
    
        #case is (x,y,c)
        else:
            iterator = len(chararray) - offset
            if offset<length:
                chararray+=chararray[iterator:iterator+length]
                chararray+=chararray[iterator:iterator+length-offset]
            else:
                chararray+=chararray[iterator:iterator+length]
            chararray += char

    out.write(chararray)

def main():
    MAX_SEARCH = 7
    fn=open("decompressed.txt","wb")
    decoder(fn, MAX_SEARCH)
    fn.close()

if __name__== "__main__":
    main()
