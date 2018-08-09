from tkinter import *
import json
import math
from analysis import *
import random
import time

WIDTH = 800
HEIGHT = 700
EDGE = 200
H = math.sqrt(3) * EDGE / 2
HALF_EDGE = EDGE / 2

SIZE = 15
LOSE = 'lose'
WIN = 'win'
TIE = 'tie'
value_to_color = {WIN: 'darkgreen', LOSE: 'red', TIE: 'yellow'}
LEFT = 'left'
RIGHT = 'right'
player_to_color = {LEFT: 'pink', RIGHT: 'blue'}
CUR_PLAYER = LEFT
INITIAL_POS = -1
POS = INITIAL_POS
PRE_POS = INITIAL_POS
MEMORANDOM = []
# Left_p = ''
# Right_p = ''
p = {LEFT: '', RIGHT: ''}

RULE = 'To move, you need to color one given line on our graph.\n' \
    'To win, you need to force your opponent to form a triangle with their lines.\n' \
       'Try to avoid forming triangles with your own line.\n' \
       'Have Fun Playing!\n '


def ShowRule():
    top = Toplevel(master)
    top.attributes('-topmost', 'true')
    top.title("rule")
    ruleMsg = Message(top, text=RULE)
    ruleMsg.pack()
    okButton = Button(top, text='OK', command=top.destroy)
    okButton.pack()
    return


'''
For the beginning page, we select players
'''


def SetPlayer():
    def setMaker():
        if right.get() != '--right player--' and left.get() != '--left player--':
            top.destroy()
            global p
            # global Right_p
            # global Left_p
            p[RIGHT] = right.get()
            p[LEFT] = left.get()
            c.itemconfig('name', text='%s V.S. %s' % (p[LEFT], p[RIGHT]))
            SetupBoard(POS)

    top = Toplevel(master)
    top.attributes('-topmost', 'true')
    top.title("chooseplayer")

    left = StringVar()
    leftOptionMenu = OptionMenu(
        top, left, '--left player--', 'human', 'DumbCom', 'PerfectCom')
    leftOptionMenu.pack()

    right = StringVar()
    rightOptionMenu = OptionMenu(
        top, right, '--right player--', 'human', 'DumbCom', 'PerfectCom')
    rightOptionMenu.pack()

    okButton = Button(top, text='OK', command=setMaker)
    okButton.pack()
    return


'''
LOAD Database from .json created by analysis.py
'''
DB = {}
with open('value.json', 'r', encoding='utf-8') as f:
    DB = json.load(f)
'''
DOTS & LINES are how we draw lines and organize them on canvas
'''
DOTS = [[WIDTH / 2 - EDGE, HEIGHT / 2],
        [WIDTH / 2 - HALF_EDGE, HEIGHT / 2 - H],
        [WIDTH / 2 + HALF_EDGE, HEIGHT / 2 - H],
        [WIDTH / 2 + EDGE, HEIGHT / 2],
        [WIDTH / 2 + HALF_EDGE, HEIGHT / 2 + H],
        [WIDTH / 2 - HALF_EDGE, HEIGHT / 2 + H]]
LINES = [DOTS[0] + DOTS[1], DOTS[1] + DOTS[2], DOTS[2] + DOTS[3],
         DOTS[3] + DOTS[4], DOTS[4] + DOTS[5], DOTS[5] + DOTS[0],
         DOTS[1] + DOTS[5], DOTS[0] + DOTS[2], DOTS[1] + DOTS[3],
         DOTS[2] + DOTS[4], DOTS[3] + DOTS[5], DOTS[4] + DOTS[0],
         DOTS[0] + DOTS[3], DOTS[1] + DOTS[4], DOTS[2] + DOTS[5]]
'''
L_COLOR is for saving line color for Passing by
'''

L_COLOR = {}

'''
For Lines, we do these things below: Click & Passby(Enter+Leave)
'''


def ClickMaker(i):
    def Click(event):
        global CUR_PLAYER
        global POS
        global PRE_POS
        global MEMORANDOM
        legalMoves = list(GenMove(POS))
        if legalMoves.count(i) != 0:
            MEMORANDOM.append(POS)
            PRE_POS = POS
            POS = DoMove(POS, i)
            if CUR_PLAYER == LEFT:
                CUR_PLAYER = RIGHT
                c.itemconfig(
                    lines[i], fill=player_to_color[LEFT], width=10)
            else:
                CUR_PLAYER = LEFT
                c.itemconfig(lines[i],
                             fill=player_to_color[RIGHT], width=10)

            SetupBoard(POS)

    return Click


def EnterLine(i):
    def Enter(event):
        global CUR_PLAYER
        global POS
        global PRE_POS
        global MEMORANDOM
        legalMoves = list(GenMove(POS))
        if legalMoves.count(i) != 0:
            c.itemconfig(lines[i], fill='gray')
        #    SetupBoard(POS)
    return Enter


def LeaveLine(i):
    def Leave(event):
        global POS
        legalMoves = list(GenMove(POS))
        if legalMoves.count(i) != 0:
            c.itemconfig(lines[i], fill=L_COLOR[str(i)])
        #   SetupBoard(POS)
    return Leave


def flipState(value):
    if value == WIN:
        return LOSE
    elif value == LOSE:
        return WIN
    else:
        return TIE


def PredictColor(nextValue):
    if nextValue == WIN:
        return value_to_color[LOSE]
    elif nextValue == LOSE:
        return value_to_color[WIN]
    else:
        return value_to_color[TIE]


def GameOver():
    def undomaker(self):
        def undo():
            self.destroy()
            Undo()
        return undo

    def resetmaker(self):
        def reset():
            self.destroy()
            Reset()
        return reset
    c.itemconfig('promt', text='%s\' win!' % CUR_PLAYER)
    top = Toplevel(master, width=200, height=70)
    top.attributes('-topmost', 'true')
    top.title("Game Over")
    ruleMsg = Message(top, text='%s\' win!' % CUR_PLAYER)
    ruleMsg.pack()
    undoButton = Button(top, text='Undo', command=undomaker(top))
    undoButton.pack()
    resetButton = Button(top, text='Reset', command=resetmaker(top))
    resetButton.pack()
    return


def SetupBoard(pos):
    # print(pos)
    if Primitive(pos) != UNDECIDED:
        GameOver()
        # print('%s win!' % CUR_PLAYER)
        return
    posStr = Pos2Str(pos)
    # print(str)
    c.itemconfig('promt', text='%s\'s turn' % CUR_PLAYER)
    moves = GenMove(pos)
    for m in moves:
        nextMove = DoMove(pos, m)
        # print(nextMove)
        value = DB[str(nextMove)][0]
        if IF_VALUE.get():  # revise
            c.itemconfig(lines[m], fill=PredictColor(
                value), width=DB[str(nextMove)][1])
            L_COLOR[str(m)] = PredictColor(value)
        else:
            c.itemconfig(lines[m], fill='black', width=10)
            L_COLOR[str(m)] = 'black'
#    print(p[CUR_PLAYER])
    if p[CUR_PLAYER] == 'DumbCom':
        # Change Stupid to Dumb
     #   print('stupid')
        ComputerGo(pos)
    elif p[CUR_PLAYER] == 'PerfectCom':
     #  print('perfect')
        PerfectGo(pos)


'''
Now for Buttons
'''


def Reset():
    global PRE_POS
    global POS
    global CUR_PLAYER
    global MEMORANDOM
    MEMORANDOM = []
    PRE_POS = INITIAL_POS
    POS = INITIAL_POS
    # print(POS)
    CUR_PLAYER = LEFT
    SetupBoard(POS)


def Undo():

    def proc():
        global PRE_POS
        global POS
        global CUR_PLAYER
        global MEMORANDOM
        if len(MEMORANDOM) == 0:
            top = Toplevel(master, width=200, height=70)
            top.attributes('-topmost', 'true')
            top.title("Warn")
            ruleMsg = Message(top, text='Undo Error')
            ruleMsg.pack()
            okButton = Button(top, text='OK', command=top.destroy)
            okButton.pack()
            return
        POS = PRE_POS
        MEMORANDOM.pop()
        PRE_POS = INITIAL_POS if len(MEMORANDOM) == 0 else MEMORANDOM[-1]
        CUR_PLAYER = LEFT if CUR_PLAYER == RIGHT else RIGHT
    if p[LEFT] != 'human' or p[RIGHT] != 'human':
        proc()
        if len(MEMORANDOM) != 0:
            proc()
    else:
        proc()
    SetupBoard(POS)


# def ValueCB():
#     print(IF_VALUE)


def ValueCBMAKER():
    # print(IF_VALUE.get())
    SetupBoard(POS)
    # return ValueCB


def ComputerGo(pos):
    moves = GenMove(pos)
    # print(moves)
    m = random.sample(list(moves), 1)[0]
    # time.sleep(0.2)
    ClickMaker(m)(1)


def PerfectGo(pos):
    moves = GenMove(pos)
    if pos == -1:
        m = random.sample(list(moves), 1)[0]
        ClickMaker(m)(1)
        return
    value = DB[str(pos)][0]
    remoteness = DB[str(pos)][1]
    for m in moves:
        nextMove = str(DoMove(pos, m))
        # print(nextMove)
        if DB[nextMove][1] == remoteness - 1 and DB[nextMove][0] != value:
            ClickMaker(m)(1)
            break


master = Tk()
master.title('Love & Hate')
IF_VALUE = BooleanVar()
c = Canvas(master, width=WIDTH, height=HEIGHT)

buttonRule = Button(master, text='Rule', command=ShowRule)
buttonRule.pack()

buttonReset = Button(master, text='Reset', command=Reset)
buttonReset.pack()

buttonUndo = Button(master, text='Undo', command=Undo)
buttonUndo.pack()

buttonValue = Checkbutton(master, text='Value&Remoteness',
                          variable=IF_VALUE, onvalue=True, offvalue=False, command=ValueCBMAKER)
buttonValue.pack()


lines = {}
for i in range(SIZE):
    lines[i] = c.create_line(LINES[i], width=10, fill='black')
    L_COLOR[str(i)] = 'black'
    c.itemconfig(lines[i], tags=(str(i) + 'tag'))
    c.tag_bind(str(i) + 'tag', sequence='<Button-1>', func=ClickMaker(i))
    c.tag_bind(str(i) + 'tag', sequence='<Enter>', func=EnterLine(i))
    c.tag_bind(str(i) + 'tag', sequence='<Leave>', func=LeaveLine(i))

SetPlayer()


c.create_text(WIDTH / 2, 25, text='%s V.S. %s' %
              (p[LEFT], p[RIGHT]), fill='black', font=('Helvetica', 30), tag='name')
c.create_text(WIDTH / 2, 60, text='%s\'s turn' %
              CUR_PLAYER, fill='black', font=('Helvetica', 30), tag='promt')
c.pack()

# ShowRule()
mainloop()
# while ((p[LEFT] == '') or (p[RIGHT] == '')):
# continue
# SetupBoard(POS)
