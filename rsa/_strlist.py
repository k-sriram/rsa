"""This module contains functions that can be used to convert strings to list of ints and reverse"""
def list2str(list_,size):
    byteval=2**8
    strlist=[]
    for i in list_:
        for j in range(size):
            strlist.append(chr(i%byteval))
            i/=byteval
    return ''.join(strlist)

def str2list(string,size):
    byteval=2**8
    list_=[]
    for i in range(0,len(string),size):
        listel=0
        for j in range(size):
            listel*=byteval
            listel+=ord(string[i+size-j-1])
        list_.append(listel)
    return list_
