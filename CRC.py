import time
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
import math

#CRC_code = [int(c) for c in (input("请输入待编码串:"))]
#CRC_mode = input("请输入CRC格式（3, 4,8,12,16,32）：")

class CRC:
    def __init__(self, CRC_code, CRC_mode):
        '''
        self.CRC_dict= {
            "3": [3, 0],
            "4": [4, 1, 0],
            "5": [5, 4, 2, 0],
            "8": [8, 2, 1, 0],
            "12": [12, 11, 3, 2, 1, 0],
            "16": [16, 15, 2, 1],
            "32": [32, 26, 23, 22, 16, 12, 11, 10, 8, 7, 5, 4, 2, 1, 0]
        }
        self.loc = self.CRC_dict[CRC_mode]
        self.crc_len = int(CRC_mode) + 1
        '''
        self.crc_len = len(CRC_mode)
        self.code_len = len(CRC_code)
        self.code = CRC_code
        self.generate_code = []
        self.check_code = []
        self.quotient = []
        #self.poly = [1 if i in self.loc else 0 for i in range(self.crc_len)][::-1]
        self.poly = CRC_mode

    def encoding(self):
        lis = [0] * (self.crc_len - 1)
        self.generate_code.extend(self.code)
        self.generate_code.extend(lis)
        pattern = self.generate_code[:self.crc_len]
        #print('{} {} {} {}'.format(len(self.generate_code), len(self.code), len(pattern), self.crc_len))
        for i in range(self.code_len):
            if pattern[0]:
                self.quotient.append(1)
                for j in range(self.crc_len - 1):
                    pattern[j] = pattern[j+1] ^ self.poly[j + 1]
            else:
                self.quotient.append(0)
                for j in range(self.crc_len - 1):
                    pattern[j] = pattern[j + 1]
            if i < self.code_len - 1:
                pattern[-1] = self.generate_code[self.crc_len + i]
        for i in range(self.crc_len - 1):
            self.check_code.append(pattern[i])
            self.generate_code[self.code_len + i] = pattern[i]

    def get_gen(self):
        return ''.join(str(i) for i in self.generate_code)

    def get_oth(self):
        return ''.join(str(i) for i in self.check_code)

    def display(self):
        code = ''.join(str(i) for i in self.code)
        poly = ''.join(str(i) for i in self.poly)
        quotient = ''.join(str(i) for i in self.quotient)
        check = ''.join(str(i) for i in self.check_code)
        generate = ''.join(str(i) for i in self.generate_code)
        print("数据为：{}\n多项式为：{}\n商为：{}\n余数为:{}\n生成码为：{}\n".format(code,poly,quotient,
                                                       check, generate))

class heming:
    def __init__(self, src_code):
        self.src_code=src_code
        self.codelen = len(src_code)
        self.bits = self.getbit()
        self.genlen = self.codelen + len(self.bits)
        self.genmap = [[] for _ in range(len(self.bits))]
        self.gen = [-1]*self.genlen
        self.check = []
        #print(self.genlen, self.bits, self.codelen, self.gen, self.genmap)

    def encoding(self):
        b=1
        for i in range(self.genlen):
            k = 1
            if i+1 not in self.bits:
                self.gen[-(i+1)] = self.src_code[-b]
                b = b+1
            for j in range(len(self.bits)):
                if (i+1) & k > 0:
                    self.genmap[j].append(i)
                k = k << 1
        #print(self.bits)
        #print(self.src_code)
        #print(self.genmap)
        #print(self.gen)
        for i in range(len(self.genmap)):
            count = 0
            for j in range(len(self.genmap[i])):
                if self.gen[-(self.genmap[i][j]+1)] == 1:
                    count = count + 1
            if count % 2 == 0:
                self.gen[-self.bits[i]] = 0
                self.check.append(0)
            else:
                self.gen[-self.bits[i]] = 1
                self.check.append(1)
        #print(self.check)
        return self.gen

    def getbit(self):
        list=[]
        i = 0
        while(2 ** i < self.codelen + i + 1):
            list.append(2 ** i)
            i = i + 1
        return list

    def checkwrong(self, check_code):
        if len(self.check) != len(check_code):
            return 0
        if self.check == check_code:
            return -1
        else:
            wrongl=[]
            for i in range(len(self.check)):
                if self.check[i] != check_code[i]:
                    wrongl.append(i)
            for i in range(self.genlen):
                wcount = 0
                for j in range(len(wrongl)):
                    if i in self.genmap[wrongl[j]]:
                        wcount = wcount + 1
                    else:
                        break
                if wcount != len(wrongl):
                    continue
                else:
                    return i + 1
            return 0


def clearcrc():
    source.delete(0, END)
    crc.delete(0, END)
    crc_result.delete(1.0, "end")
    sourcej.delete(0, END)
    crcj.delete(0, END)
    crcj_result.delete(1.0, "end")

def calculate():
    src = [int(c) for c in source.get()]
    cr  = [int(c) for c in crc.get()]
    for i in range(len(src)):
        if src[i] >1:
            clearcrc()
            crc_result.insert('insert', "only 0 and 1")
            return 1
    if cr[0] == 0:
        clearcrc()
        crc_result.insert('insert', "need 1 at top")
        return 1
    if cr[-1] == 0:
        clearcrc()
        crc_result.insert('insert', "need 1 at low")
        return 1
    for i in range(len(cr)):
        if cr[i] > 1:
            clearcrc()
            crc_result.insert('insert', "only 0 and 1")
            return 1
    solver = CRC(src, cr)
    solver.encoding()
    output = solver.get_gen()
    crc_result.delete(1.0, "end")
    crc_result.insert('insert', output)
    return 1


def decoding():
    cr = [int(c) for c in crcj.get()]
    src = [int(c) for c in sourcej.get()][:-len(cr)+1]
    other = [int(c) for c in sourcej.get()][len(sourcej.get()) - len(cr) + 1:]
    for i in range(len(src)):
        if src[i] >1:
            clearcrc()
            crcj_result.insert('insert', "only 0 and 1")
            return 1
    if cr[0] == 0:
        clearcrc()
        crcj_result.insert('insert', "need 1 at top")
        return 1
    if cr[-1] == 0:
        clearcrc()
        crcj_result.insert('insert', "need 1 at low")
        return 1
    for i in range(len(cr)):
        if cr[i] > 1:
            clearcrc()
            crcj_result.insert('insert', "only 0 and 1")
            return 1
    for i in range(len(other)):
        if other[i] >1:
            clearcrc()
            crcj_result.insert('insert', "only 0 and 1")
            return 1
    solver = CRC(src, cr)
    solver.encoding()
    check = solver.get_oth()
    if check == ''.join(str(i) for i in other):
        crcj_result.delete(1.0, "end")
        crcj_result.insert('insert', ''.join(str(i) for i in src))
    else:
        crcj_result.delete(1.0, "end")
        crcj_result.insert('insert', 'got a wrong code')
    return 1

def hcalculate():
    src = [int(c) for c in hsource.get()]
    for i in range(len(src)):
        if src[i] >1:
            hclearcrc()
            hcrc_result.insert('insert', "only 0 and 1")
            return 1
    hm = heming(src)
    gen = hm.encoding()
    hcrc_result.delete(1.0, "end")
    hcrc_result.insert('insert', ''.join(str(c) for c in gen))
    return 1

def hclearcrc():
    hsource.delete(0, END)
    hcrc_result.delete(1.0, "end")
    hsourcej.delete(0, END)
    hcrcj_result.delete(1.0, "end")
    return

def hdecoding():
    src = [int(c) for c in hsourcej.get()]
    for i in range(len(src)):
        if src[i] >1:
            hclearcrc()
            hcrcj_result.insert('insert', "only 0 and 1")
            return 1
    check_code = []
    bits = []
    i = 0
    while 2 ** i < len(src) + 1:
        bits.append(2 ** i)
        i = i + 1
    for i in range(len(bits)):
        check_code.append(src.pop(-bits[i]+i))
    hm = heming(src)
    gen = hm.encoding()
    result = hm.checkwrong(check_code)
    if result == -1:
        hcrcj_result.delete(1.0, "end")
        hcrcj_result.insert('insert', ''.join(str(c) for c in src))
    elif result != 0:
        hcrcj_result.delete(1.0, "end")
        hcrcj_result.insert('insert', "position [{}] is wrong".format(str(result)))
    else:
        hcrcj_result.delete(1.0, "end")
        hcrcj_result.insert('insert', "num of bits wrong")
    return


root =Tk()
root.geometry("1000x300")

#标签
L_titile = Label(root,text='CRC编码')
L_titile.config(font='Helvetica -15 bold',fg='blue')
L_titile.place(x=100,y=20,anchor="center")

jiema = Label(root,text='CRC解码')
jiema.config(font='Helvetica -15 bold',fg='blue')
jiema.place(x=350,y=20,anchor="center")

s_input = Label(root, text='输入源码')
s_input.place(x=0, y=50)
c_input = Label(root, text='输入校验')
c_input.place(x=0, y=100)
s_output = Label(root, text='输出结果')
s_output.place(x=0, y=200)

sjiema_input = Label(root, text='输入接收')
sjiema_input.place(x=250, y=50)
cjiema_input = Label(root, text='输入校验')
cjiema_input.place(x=250, y=100)
sjiema_output = Label(root, text='解码结果')
sjiema_output.place(x=250, y=200)
#按钮
B_0 = Button(root, text="计算CRC", command=calculate)
B_0.place(x=50,y=250)
B_1 = Button(root, text="清除CRC", command=clearcrc)
B_1.place(x=200,y=250)
B_3 = Button(root, text="解码CRC", command=decoding)
B_3.place(x=300,y=250)
source = tk.Entry(root, show = None)
source.place(x=50, y=50)
crc = tk.Entry(root, show = None)
crc.place(x=50, y=100)

sourcej = tk.Entry(root, show = None)
sourcej.place(x=300, y=50)
crcj = tk.Entry(root, show = None)
crcj.place(x=300, y=100)

crc_result = tk.Text(root, height=2,width=20)
crc_result.place(x=50, y=200)
crcj_result = tk.Text(root, height=2,width=20)
crcj_result.place(x=300, y=200)



h_titile = Label(root,text='海明编码')
h_titile.config(font='Helvetica -15 bold',fg='blue')
h_titile.place(x=600, y=20,anchor="center")

hjiema = Label(root,text='海明解码')
hjiema.config(font='Helvetica -15 bold',fg='blue')
hjiema.place(x=850, y=20,anchor="center")

hs_input = Label(root, text='输入源码')
hs_input.place(x=500, y=50)
hs_output = Label(root, text='输出结果')
hs_output.place(x=500, y=200)

hsjiema_input = Label(root, text='输入接收')
hsjiema_input.place(x=750, y=50)
hsjiema_output = Label(root, text='解码结果')
hsjiema_output.place(x=750, y=200)
#按钮
hB_0 = Button(root, text="计算海明", command=hcalculate)
hB_0.place(x=550,y=250)
hB_1 = Button(root, text="清除海明", command=hclearcrc)
hB_1.place(x=700,y=250)
hB_3 = Button(root, text="解码海明", command=hdecoding)
hB_3.place(x=850,y=250)

hsource = tk.Entry(root, show = None)
hsource.place(x=550, y=50)
hsourcej = tk.Entry(root, show = None)
hsourcej.place(x=800, y=50)


hcrc_result = tk.Text(root, height=2,width=20)
hcrc_result.place(x=550, y=200)
hcrcj_result = tk.Text(root, height=2,width=20)
hcrcj_result.place(x=800, y=200)
root.mainloop()
#crc = CRC(CRC_code, CRC_mode)
#crc.encoding()
#crc.display()











