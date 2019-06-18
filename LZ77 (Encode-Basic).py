#File handling
f = open('LZZ.txt','r')
str = f.read()
print (str)

#LZ77 Encoding
win_size = 13
search_size = 7
look_a = 6
l = len(str)
cnt = -1
s_b = ""
h=0
while s_b != str[l-search_size:l] :
    i=0
    length = 0
    if cnt + look_a<=l :
        para = look_a
    else :
        para = l-cnt
    while para > i and cnt >= 0 :
        t = str [cnt : para + cnt -i]
        if s_b.find(t) != -1 :
            a = [m.start() for m in re.finditer(t,s_b)]
            off = len(s_b) - a[-1]
            length = len (t)
            code = str [para + cnt -i]
            cnt+=len(t)
            cnt+=1
            print (off,length,code)
            break
        i+=1
    if i==para or cnt<0:
        cnt+=1
        if cnt<=l-1 :
            print (0,0,str[cnt])
    if cnt>search_size :
        h = cnt - search_size
    s_b  = str [h : cnt]