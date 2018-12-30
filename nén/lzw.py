import numpy as np
from PIL import Image
import io
import struct

def convert_to_byte(a,b):
    ab = (a<<12)|b
    three_bytes = ab.to_bytes(3,byteorder='big')
    return three_bytes
def convert_to_string(ab):
    a = ab>>12
    b = ab & ((1 << 12) - 1)
    return a,b

def lzw_compression(Filename):
    # open file 
    matrix = np.asarray(Image.open(Filename))
#    print(matrix.shape)
    string_matrix = []
    row = matrix.shape[0]
    clum = matrix.shape[1]
    x = matrix.shape[2]

    # convert matrix to string array
    for i in range(0,row):
        for j in range(0,clum):
            for z in range(0,x):
                string_matrix.append(str(int(matrix[i,j,z])))
#    print(len(string_matrix))
    dict_matrix =[]
    for i in range(0,257):
        dict_matrix.append(str(int(i)))
    # string_matrix = []
    MAX = 4095
    result =[]

    # conpresstion
    print ("Đang nén ...")
    s = string_matrix[0]
    i = 1
    k = len(string_matrix)
    print ("Waiting ...")
    while i in range(0,k):
        c = string_matrix[i]
        if s +'-'+ c in dict_matrix:
            s = s +'-'+ c
        else:
            if len(dict_matrix)>MAX:
                del(dict_matrix[257:])
                result.append(256)
                i = i - len(s.split("-"))+1 
#                print("lend ",len(s.split("-")))
                s = s.split('-')[0]
                continue 
            result.append(int(dict_matrix.index(s)))
            dict_matrix.append(s +'-'+c)
            s = c
        i = i + 1 
    
    result.append(int(dict_matrix.index(s)))
    result.append(str(int(row)))
    result.append(str(int(clum)))
    result.append(str(int(x)))
    print("Chiều dài string_maxtrix ban đầu: ", len(string_matrix))
    print("Chiều result: ", len(result))

    
    # save file 
    result_byte = "".encode()
    i = 0
    if len(result)%2==0: size = len(result)
    else: size = len(result)-1
    while i in range(0,size):
        result_byte += convert_to_byte(int(result[i]),int(result[i+1]))
        i += 2
    if len(result) %2 ==1:
        temp = (int(result[len(result)-1])<<12).to_bytes(3,byteorder='big')
        result_byte+=temp
    file = open(Filename + '_lzw.bin','wb')
    file.write(result_byte)
    file.close()
    print ("Hoàn tất ...")

#    return dict_matrix
    return Filename +'_lzw.bin'
def lzw_decompression(Filename):
    #read file

    file = open(Filename,'rb')
    string = file.read()
    file.close()
    get_bin = lambda x, n: format(x, 'b').zfill(n)
    i = 0
    list_matrix = []
    while i in range(len(string)):
        string_byte = str(get_bin(string[i],8))+ str(get_bin(string[i+1],8))+str(get_bin(string[i+2],8))
        a ,b = convert_to_string(int(string_byte,2))
        list_matrix.append(int(a))
        list_matrix.append(int(b))
        i +=3

    d = list_matrix[len(list_matrix)-1]
    if(d==0):
        del(list_matrix[len(list_matrix)-1])
        d = list_matrix[len(list_matrix)-1]

    for i in range(0,len(list_matrix)):
        list_matrix[i]= str(list_matrix[i])


    k = len(list_matrix)
    z = int(list_matrix[k-1])
    c = int(list_matrix[k-2])
    d = int(list_matrix[k-3])
    print(z)
    print(c)
    print(d)
    del(list_matrix[k-3:])
    
    # creating original dictionary 

    dict_matrix =[]
    for i in range(0,256):
        dict_matrix.append(str(int(i)))
    dict_matrix.append(str(int(256)))
    s = None
    this_CC = False 
    result =[]
    k=0

    # Decompression
    print("Đang giải nén ...")
    print("Waiting ...")
    while k in range(len(list_matrix)):
        i = list_matrix[k]
        if(i == str(int(256))):
            k += 1
            i = list_matrix[k]
            this_CC = True
        if(len(dict_matrix)-1<int(i)):
            entry= None
        else :
            entry = dict_matrix[int(i)]
        if entry == None:
            temp = s.split('-')
            entry = s+'-'+temp[0]
        result.append(entry)
        if s!=None:
            temp = entry.split('-')
            dict_matrix.append(str(s) +'-'+temp[0])
        s = entry 
        if this_CC: 
            this_CC = False
            del(dict_matrix[257:])
        k += 1

    # seperation 
    string_matrix = []
    for i in result:
        seq = i.split('-')
        for j in seq:
            string_matrix.append(j)
    arr = np.zeros((d,c,z))
    idx = 0
    for i in range(0,d):
        for j in range(0,c):
            for k in range(0,z):
                arr[i,j,k] = string_matrix[idx]
                idx +=1
    im = Image.fromarray(np.uint8(arr))
    im.save(Filename.replace("_lzw.bin","_lzw_decode")+".bmp")
    im.show()
    print ("Hoàn tất ...")

#    return dict_matrix
    return Filename.replace("_lzw.bin","_lzw_decode")+".bmp"

#compression('flying.bmp')
#decompression('flying.bmp.bin')
#print('done')
    