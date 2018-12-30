from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
import urllib3
import IPython, time
import os


def get_matrix_image(url):
    im = Image.open(url)
    np_im = np.array(im)
    return np_im
        
def cal(matrix):
    hist = {}
    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            for k in range(0, matrix.shape[2]):
                hist[matrix[i][j][k]] =  hist.get(matrix[i][j][k],0) + 1
    return hist
def getHigh(url):
    return get_matrix_image(url).shape[0]
def getWeight(url):
    return get_matrix_image(url).shape[1]
def getShape(url):
    return get_matrix_image(url).shape[2]
def sortFreq (vector) :
    value = vector.keys()
    tuples = []
    for i in value :
        tuples.append((vector[i],i))
    tuples.sort()
    return tuples

def getKey(tuple):
    return tuple[0]

def getValue(tuple):
    return tuple[1]

def buildTree(vector):
    while len(vector) > 1:
        lowestTwo = tuple(vector[0:2])
        theRest = vector[2:]
        sumPro = lowestTwo[0][0] + lowestTwo[1][0]
        vector = theRest + [(sumPro, lowestTwo)]
        sorted(vector, key = getKey)
    return vector[0]

def Tree(tree):
    a = 3
    a = np.dtype('uint8').type(a)
    p = tree[1]
    if type(p) == type(a): 
        return p
    else:
        return (Tree(p[0]), Tree(p[1]))
code= {}
def assignCodes(n, pat = ''):
    a = 3
    a = np.dtype('uint8').type(a)
    
    if type(n) == type(a):
        code[n] = pat
    else:
        assignCodes(n[0], pat+"0")
        assignCodes(n[1], pat+"1")
    

def pad_encoded_text(encoded_text):
    extra_padding = 8 - len(encoded_text) % 8
    for i in range(extra_padding):
        encoded_text += "0"

    padded_info = "{0:08b}".format(extra_padding)
    encoded_text = padded_info + encoded_text
    return encoded_text

def get_byte_array(padded_encoded_text):
    if(len(padded_encoded_text) % 8 != 0):
        print("Encoded text not padded properly")
        exit(0)

    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i+8]
        b.append(int(byte, 2))
    return b

def encode(code, vector):
    file = open("text_code.txt","w+")
    for i in range(0, vector.shape[0]):
        for j in range(0, vector.shape[1]):
            for k in range(0, vector.shape[2]):
                file.write(code[vector[i][j][k]])
    file.close()
    
def read(path):
    file = open("text_code.txt", "r")
    t = pad_encoded_text(file.read())
    file.close()
    b = get_byte_array(t)
    file_name_out = path + "_hm.bin"
    file = open(file_name_out,"wb")
    file.write(bytes(b))
    file.close()
    return file_name_out
    
def read_file(filename):
    file = open(filename, 'rb')
    bit_string = ""
    byte = file.read()
    for i in byte:
        bits = bin(i)[2:].rjust(8, '0')
        bit_string += bits
    # loại bỏ các ký tự fix size ở cuối của string 
    fixed_size = bit_string[:8]
    fixed_size = int(fixed_size, 2)
    encoded_text = bit_string[8:] 
    encoded_text = encoded_text[:-1*fixed_size]
    # trả về string nhị phân
    return encoded_text
    pass

def decode(tree, str, path):
    a = 3
    high = getHigh(path[0:len(path)- 7])
    weight = getWeight(path[0:len(path) - 7])
    shape = getShape(path[0:len(path) - 7])
    output = np.zeros((high,weight,shape))
    output = np.uint8(output)
    k =0
    j = 0
    n = 0
    p = tree
    for i in str:
        if j == weight:
            j = 0
            k+=1
        if n == shape:
            j+=1
            n = 0
        if i == '0': p = p[0]
        else: p = p[1]
        if type(p) == type(a):
            p = np.dtype('uint8').type(p)
            output[k][j][n] = p
            n+=1
            p = tree
    return output

def hm_compression(path):
    print("Waiting ...")
    matrix = get_matrix_image(path)
    hist = cal(matrix)
    sorted_hist = sortFreq(hist)
    tree = buildTree(sorted_hist)
    trim = Tree(tree)
    assignCodes(trim)
    file = open(path + "_hmtree.txt", "w")
    file.write(str(trim))
    file.close()
    encode(code,matrix)
    t = read(path)
    os.remove("text_code.txt")
    return t

##print(t)
def hm_decompression(path):
    print("Waiting ...")
    file = open(path[0:len(path) - 7] + "_hmtree.txt","r")
    trim = file.read()
    file.close()
    trim = eval(trim)
    bit_string = read_file(path)
#    print(path)
    ot = decode(trim, bit_string, path)
    ot = np.array(ot)
    new_im = Image.fromarray(ot)
    file_image = path.replace(".bin","") + "_decode.bmp"
    new_im.save(file_image)
    new_im.show()    
    return file_image
#p = decompression("flying.bmp_hm.bin")
#print(p)