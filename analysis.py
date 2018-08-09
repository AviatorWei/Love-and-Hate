'''
fuction isPrimitive is not completely checked
'''

from math import *
import numpy as np
import json
import sys

SIZE = 15
REARRANGE = np.zeros((SIZE + 1, SIZE + 1, SIZE + 1))
# REARRANGE = []
# position in [0, POS_COUNT)
POS_COUNT = 3492116
POS2STR = {}
STR2POS = {}
VALUE = {}
PRIMITIVE = [[0, 6, 5], [1, 7, 0], [2, 8, 1], [3, 9, 2], [4, 10, 3], [5, 11, 4],
             [7, 5, 14], [8, 0, 12], [9, 1, 13], [
                 10, 2, 14], [11, 3, 12], [6, 4, 13],
             [5, 12, 10], [0, 13, 11], [1, 14, 6], [
                 2, 12, 7], [3, 13, 8], [4, 14, 9],
             [6, 8, 10], [7, 9, 11]]
WIN = 'win'
LOSE = 'lose'
UNDECIDED = 'undecided'
TIE = 'tie'

COUNT = 0

visited = [0]*POS_COUNT
root = [0]*POS_COUNT

LOAD = True

def init():
    global REARRANGE, POS2STR, STR2POS
    if LOAD:
    	REARRANGE = np.load('rearrange.npy')
    # with open('pos2str.json', 'r', encoding='utf-8') as psf:
    #     POS2STR = json.load(psf)
    # with open('str2pos.json', 'r', encoding='utf-8') as spf:
    #     str2pos = json.load(spf)


'''
Rearrange(T, A, B) is the number of combinations of A 1s and B 2s in T positions
'''


def Rearrange(T, A, B):
    global REARRANGE
    if REARRANGE[T][A][B] == 0:
        REARRANGE[T][A][B] = factorial(
            T) / (factorial(A) * factorial(B) * factorial(T - A - B))
        return REARRANGE[T][A][B]
    else:
        return REARRANGE[T][A][B]


'''
compute all REARRANGE and store it to rearrange.npy
'''


def CreateRearrange(size):
    for t in range(1, size + 1):
        for a in range(0, t + 1):
            for b in range(0, t - a + 1):
                Rearrange(t, a, b)
    np.save('rearrange.npy', REARRANGE)


'''
compute the smaller upperbound
'''


def PosUpperBound(SIZE):
    n = 0
    for i in range(1, SIZE + 1):
        n += Rearrange(SIZE, ceil(i / 2), floor(i / 2))
    return n


'''
create a string from pos, T, A, B
'''


def MyString(pos, T, A, B):
    if T == 1:
        if A == 1:
            return '1'
        elif B == 1:
            return '2'
        else:
            return '0'

    if T > A + B:
        if pos < Rearrange(T - 1, A, B):
            return '0' + MyString(pos, T - 1, A, B)
        else:
            pos -= Rearrange(T - 1, A, B)

    if A > 0:
        if pos < Rearrange(T - 1, A - 1, B):
            return '1' + MyString(pos, T - 1, A - 1, B)
        else:
            pos -= Rearrange(T - 1, A - 1, B)

    if B > 0:
        return '2' + MyString(pos, T - 1, A, B - 1)


'''
transfer number to string
'''


def Pos2Str(pos):
    if pos == -1:
        return '0' * 15
    str = '0' * SIZE
    # return str
    n = 0
    for i in range(1, SIZE + 1):
        if pos >= Rearrange(SIZE, floor(i / 2), ceil(i / 2)):
            pos -= Rearrange(SIZE, floor(i / 2), ceil(i / 2))
        else:
            n = i
            break
    return MyString(pos, SIZE, floor(n / 2), ceil(n / 2))


'''
transfer str to pos
'''


def Str2Pos(str):
    if str == '000000000000000':
        return -1
    T = SIZE
    A = str.count('1')
    B = str.count('2')
    pos = 0
    for i in range(1, A + B):
        pos += Rearrange(T, floor(i / 2), ceil(i / 2))
    for i in range(15):
        if str[i] == '0':
            pos += 0
        else:
            pos += Rearrange(T - 1, A, B) if T > A + B else 0
            if str[i] == '1':
                A -= 1
            else:
                pos += Rearrange(T - 1, A - 1, B) if A > 0 else 0
                B -= 1
        T -= 1
    return int(pos)


'''
compute hash and store them to file
'''


def HashFile():
    myHash = {}
    for i in range(POS_COUNT):
        str = Pos2Str(i)
        myHash[i] = str
    jsonHash = json.dumps(myHash)
    with open('hash.json', 'r', encoding='utf-8') as f:
        # f.write(jsonHash)
        myHash = json.load(f)
    reverseMyHash = {}
    for key, value in myHash.items():
        reverseMyHash[value] = key
    jsonReverse = json.dumps(reverseMyHash)
    with open('str2pos.json', 'w', encoding='utf-8') as f2:
        f2.write(jsonReverse)
    return myHash


'''
compute all symmetry for pos
'''


def Permutation(pos):
    result = []
    str = Pos2Str(pos)
    a = str[:6]
    b = str[6:12]
    c = str[12:15]
    # print(a)
    # print(b)
    # print(c)
    # print(str)
    for i in range(5):
        a = a[1:6] + a[0]
        b = b[1:6] + b[0]
        c = c[1:3] + c[0]
        result.append(a + b + c)
    result = list(map(Str2Pos, result))
    # print(result)
    return result


def Symmetry(pos):
    switch = [5,4,3,2,1,0,6,11,10,9,8,7,12,14,13]

    s = Pos2Str(pos)
    # print(s)
    l = []
    for i in range(15):
    	l.append(s[switch[i]])
    newS =''.join(l)
    # print(newS)
    return Str2Pos(newS)

def isPrimitive(pos):
    str = Pos2Str(pos)
    result = False
    for state in PRIMITIVE:
        edgeState = [str[i] for i in state]
        if ('1' in edgeState) or ('0' in edgeState):
            continue
        else:
            result = True
            break
    return result


def Primitive(pos):
    if isPrimitive(pos):
        return WIN
    if '0' not in Pos2Str(pos):
        return TIE
    else:
        return UNDECIDED


def GenMove(pos):
    str = Pos2Str(pos)
    return filter(lambda i: str[i] == '0', range(15))


def DoMove(pos, m):
    str = Pos2Str(pos)
    # str = str[:m] + '1' + str[m:SIZE]
    edgeList = list(str)
    edgeList[m] = '1'
    for i in range(SIZE):
        if edgeList[i] == '1':
            edgeList[i] = '2'
        elif edgeList[i] == '2':
            edgeList[i] = '1'
    # str[m] = '1'
    str = ''.join(edgeList)
    return Str2Pos(str)


def Solve(pos):
	global COUNT
	if pos in VALUE:
		return VALUE[pos]
	elif Primitive(pos) != UNDECIDED:
        # print(pos)
		VALUE[pos] = (Primitive(pos), 0)
		for p in Permutation(pos):
			VALUE[p] = (Primitive(pos), 0)
		sym = Symmetry(pos)
		if sym not in VALUE:
			VALUE[sym]=(Primitive(pos), 0)
			for p in Permutation(sym):
				VALUE[p] = (Primitive(pos), 0)
	else:
        # print(pos)
		moves = list(GenMove(pos))
		next = [DoMove(pos, m) for m in moves]
		results = {}
		for p in next:
			v, r = Solve(p)
            # print(p)
			if v not in results:
				results[v] = r
			else:
				results[v] = max(r, results[v]) if (
                    v == WIN or v == TIE) else min(r, results[v])
		if LOSE in results:
			VALUE[pos] = (WIN, results[LOSE] + 1)
			for p in Permutation(pos):
				VALUE[p] = (WIN, results[LOSE] + 1)
			sym = Symmetry(pos)
			if sym not in VALUE:
				VALUE[sym]=(WIN, results[LOSE] + 1)
				for p in Permutation(sym):
					VALUE[p] = (WIN, results[LOSE] + 1)
		elif TIE in results:
			VALUE[pos] = (TIE, results[TIE] + 1)
			for p in Permutation(pos):
				VALUE[p] = (TIE, results[TIE] + 1)
			sym = Symmetry(pos)
			if sym not in VALUE:
				VALUE[sym]=(TIE, results[TIE] + 1)
				for p in Permutation(sym):
					VALUE[p] = (TIE, results[TIE] + 1)
		else:
			VALUE[pos] = (LOSE, results[WIN] + 1)
			for p in Permutation(pos):
				VALUE[p] = (LOSE, results[WIN] + 1)
			sym = Symmetry(pos)
			if sym not in VALUE:
				VALUE[sym]=(LOSE, results[WIN] + 1)
				for p in Permutation(sym):
					VALUE[p] = (LOSE, results[WIN] + 1)
	COUNT+=1
	return VALUE[pos]

def Visit(pos):
	global COUNT
	if visited[pos] == 0:
		print(pos)
		COUNT+=1
		visited[pos]=1
		for p in Permutation(pos):

			visited[p] = 1
		for p in Permutation(Symmetry(pos)):
			# next=DoMove(pos, m)
			visited[p]=1
		if Primitive(pos)==UNDECIDED:
			for m in GenMove(pos):
				n = DoMove(pos, m)
				Visit(n)

def SetRoot(pos):
	global COUNT
	print(pos)
	COUNT+=1
	root[pos] = pos
	for p in Permutation(pos):
		root[p] = pos
	sym = Symmetry(pos)
	if root[sym]==0:
		root[sym] = pos
		for p in Permutation(sym):
			root[p] = pos
	if Primitive(pos)!=UNDECIDED:
		return
	moves = GenMove(pos)
	for m in moves:
		if m>11:
			n = DoMove(pos, m)
			if root[n]==0 and n!=0:
				SetRoot(n)


def CauseError():
    r = 1 / 0
    return r


if __name__ == '__main__':

    init()
    # print(Pos2Str(-1))

    if len(sys.argv)>1:
    	if sys.argv[1]=='init':
    		# global LOAD
    		LOAD = False
    		CreateRearrange(SIZE)
		    for i in range(POS_COUNT):
		    	Solve(i)
		    valueJson = json.dumps(VALUE)
		    with open('value.json', 'w', encoding='utf-8') as f:
		        f.write(valueJson)
    # compute all rearrange for size 15 and store it to file
    # CreateRearrange(SIZE)
    	else:
    		print('Error: Option %s does not exist!' % sys.argv[1])
    # print(Pos2Str(1))

    # compute the upper bound of positions
    # posCount = PosUpperBound(SIZE)

    # store hash in files
    # HashFile()

    # Permutation(2999)

    # check if function Str2Pos is correct
    # for i in range(POS_COUNT):
    #     if Str2Pos(Pos2Str(i)) != i:
    #         print(i)
    #         print(Str2Pos(Pos2Str(POS_COUNT)))
    #         CauseError()

    # test function isPrimitive
    # print(isPrimitive(98489))
    # print(Pos2Str(0))
    # print(Str2Pos('000000000000000'))
    # print(Str2Pos('022001002001100'))
    # print(Primitive(98489))

    # test Symmetry
    # Symmetry(200)

    # test function GenMove
    # print(Pos2Str(2))
    # print(Pos2Str(18))
    # print(Pos2Str(226))
    # for m in GenMove(1000):
    #     print(m)
    # print(GenMove(1000))
    # print(Solve(2123439))

    # test function Solve
    # print(Str2Pos('000000000000100'))
    # SetRoot(14)
    # print(Permutation(3053312))
    # SetRoot(8)
    # SetRoot(2)
    # print('-----')
    # print(COUNT)
    # for i in range(POS_COUNT):
    # # print(i)
    # 	Solve(i)
    # # # Solve(0)
    # valueJson = json.dumps(VALUE)
    # with open('value.json', 'w', encoding='utf-8') as f:
    #     f.write(valueJson)
    # c = 0
    # with open('temp.txt', 'r', encoding = 'utf-8') as f:
    # 	poses = f.read().split('\n')
    # # poses = np.load('temp.txt')
    # for i in poses:
    # 	if Primitive(int(i))!=UNDECIDED:
    # 		c+=1
    # print(c)

'''
174935
536
3
'''
