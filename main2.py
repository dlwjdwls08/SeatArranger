import datetime
import os
import random
import time
import tkinter as tk
from tkinter import CENTER, ttk, messagebox, filedialog, scrolledtext, font, colorchooser
from typing import Literal
from PIL import Image, ImageDraw, ImageFont, ImageTk

win = tk.Tk('자리배치', '자리배치')
win.title('자리배치')
win.geometry("500x500")
NoteBook = ttk.Notebook(win)
MainTab = ttk.Frame(win,name='main')
win.iconphoto(False, tk.PhotoImage(file='util/chair.png', master=win))

def IntCheck(var:tk.StringVar, reset:int, func):
    def inner(event):
        if (not var.get().isdigit()):
            var.set(reset)
            messagebox.showerror('잘못된 값', '자연수를 입력해주세요')
        func()
        UpdateSeatLabelFrame()

    return inner


GreenStyle = ttk.Style()
GreenStyle.map('G.TButton', background=[('active', '#000fff000')])
SettingLabelFrame = ttk.Labelframe(win, name='setting', height=100, text='설정')
SeatLabelFrame = ttk.Labelframe(win, name='seat', height=300, text='자리')
Column = tk.StringVar(value=1)
Row = tk.StringVar(value=1)
Number = tk.StringVar(value=1)
MemberList = ['1번']
Seat = [['.']]
def SeatButtonCommand(x, y):
    def inner():
        if (Seat[x][y] == '.'):
            Seat[x][y] = '-'
        else:
            Seat[x][y] = '.'
        UpdateSeatLabelFrame()
    return inner
def UpdateSeatLabelFrame():
    for child in SeatLabelFrame.winfo_children():
        child.destroy()
    ttk.Label(SeatLabelFrame, text='교탁', borderwidth=1, relief='groove', anchor=tk.CENTER).place(relx=0.5, rely=0, anchor=tk.N, relwidth=0.4, relheight=1/(int(RowSpinbox.get())*2+1)/1.5)
    for i in range(int(RowSpinbox.get())):
        for j in range(int(ColumnSpinbox.get())):
            b = tk.Button(SeatLabelFrame, text='-' if Seat[i][j] == '.' else 'X', command=SeatButtonCommand(i, j), relief='groove', background='#c2f1f5' if Seat[i][j] == '.' else '#f5c2c2')
            b.place(relwidth=1/(int(ColumnSpinbox.get())*2),relheight=1/(int(RowSpinbox.get())*2+1),relx = (1/(int(ColumnSpinbox.get()) + 1) * (j+1)), rely=(1 / (int(RowSpinbox.get())+1) * (i+1)), anchor=tk.CENTER)

def NumberSpinboxCommand():
    while (int(NumberSpinbox.get()) > len(MemberList)):
        MemberList.append(f'{len(MemberList) + 1}번')
    while (int(NumberSpinbox.get()) < len(MemberList)):
        MemberList.pop()
    UpdateSeatLabelFrame()
def RowSpinboxCommand():
    while (int(RowSpinbox.get()) > len(Seat)):
        Seat.append(['.' for i in range(int(ColumnSpinbox.get()))])
    while (int(RowSpinbox.get()) < len(Seat)):
        Seat.pop()
    UpdateSeatLabelFrame()
def ColumnSpinboxCommand():
    for i in range(len(Seat)):
        while (int(ColumnSpinbox.get()) > len(Seat[i])):
            Seat[i].append('.')
        while (int(ColumnSpinbox.get()) < len(Seat[i])):
            Seat[i].pop()
    UpdateSeatLabelFrame()
RowLabel = ttk.Label(SettingLabelFrame, text='행:', justify='center')
RowLabel.place(relx=0.1)
RowSpinbox = ttk.Spinbox(SettingLabelFrame, textvariable=Row, width=5,from_=1, to=1000000, increment=1, command=RowSpinboxCommand)
RowSpinbox.place(relx=0.2)
RowSpinbox.bind("<FocusOut>", IntCheck(Row, 1, RowSpinboxCommand))
ttk.Label(SettingLabelFrame, text='열:', justify='center').place(relx=0.4)
ColumnSpinbox = ttk.Spinbox(SettingLabelFrame, textvariable=Column, width=5,from_=1, to=1000000, increment=1, command=ColumnSpinboxCommand)
ColumnSpinbox.place(relx=0.5)
ColumnSpinbox.bind("<FocusOut>", IntCheck(Column, 1, ColumnSpinboxCommand))
ttk.Label(SettingLabelFrame, text='인원수:', justify='center').place(relx=0.7)
NumberSpinbox = ttk.Spinbox(SettingLabelFrame, width=5, textvariable=Number,from_=1, to=1000000, increment=1, command=NumberSpinboxCommand)
NumberSpinbox.place(relx=0.8)
NumberSpinbox.bind("<FocusOut>", IntCheck(Number, 1, NumberSpinboxCommand))
def DetailMemberButtonCommand():
    global Number, MemberList
    dwin = tk.Tk('세부설정', '세부설정')
    dwin.title('세부설정')
    dwin.geometry('300x300')
    dwin.iconphoto(False, tk.PhotoImage(file='util/chair.png', master=dwin))
    def SubmitButtonCommand():
        MemberList.clear()
        for m in Input.get("1.0", tk.END).split('\n'):
            if (not m):
                continue
            MemberList.append(m)
        Number.set(len(MemberList))
        dwin.destroy()
    SubmitButton = tk.Button(dwin, text='완료', command=SubmitButtonCommand, relief='groove')
    SubmitButton.pack(fill='x', side='bottom', expand=1)
    Input = scrolledtext.ScrolledText(dwin, padx=3, pady=3, font=font.Font(family='@맑은 고딕', size=18))
    Input.pack(fill='both', side='top', expand=1, padx=10, ipadx=10, pady=10)
    for m in MemberList:
        Input.insert(tk.END, f'{m}\n')
    dwin.mainloop()

UpdateSeatLabelFrame()

DetailMemberButton = tk.Button(SettingLabelFrame, text='세부설정', command=DetailMemberButtonCommand, relief='groove')
DetailMemberButton.place(relx=0.75, rely=0.3)

def SettingSaveButtonCommand():
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    fn = filedialog.asksaveasfilename(filetypes=(('Seat Arranger Setting Files', '*.sasf'),), title='Save Setting as', initialdir='./loader', initialfile=now.strftime("%Y-%m-%d-%H-%M-%S"))
    if (not fn):
        return
    f = open(f'{fn}.sasf', 'w', encoding='utf-8')
    #f.write('SASF\n')#Seat Arranger Setting File
    f.write(f'{Row.get()} {Column.get()} {Number.get()}\n')
    for i in Seat:
        for j in i:
            f.write(f'{j} ')
        f.write('\n')
    for i in MemberList:
        f.write(f'{i}\n')
    f.close()
def SettingLoadButtonCommand():
    fn = filedialog.askopenfilename(filetypes=(('Seat Arranger Setting Files', '*.sasf'), ), title='Open Setting as', initialdir='./loader')
    if (not fn):
        return
    f = open(fn, 'r', encoding='utf-8')
    #l = f.readline().rstrip('\n')
    #if (l != 'SASF'):
    #    return messagebox.showerror('잘못된 파일', '자리배치 설정 파일이 아닙니다.')
    l = f.readline().rstrip('\n').split()
    Row.set(l[0]), Column.set(l[1]), Number.set(l[2])
    Seat.clear()
    for i in range(int(Row.get())):
        Seat.append(list(f.readline().rstrip('\n').split()))
    MemberList.clear()
    for i in range(int(Number.get())):
        MemberList.append(f.readline().rstrip('\n'))
    UpdateSeatLabelFrame()
    f.close()

SettingSaveButton = tk.Button(win, command=SettingSaveButtonCommand, text='설정 저장', relief='groove')
SettingSaveButton.place(relx=0.2, rely=0.9, relwidth=0.2, relheight=0.08, anchor=tk.CENTER)

SettingLoadButton = tk.Button(win, text='설정 불러오기', command=SettingLoadButtonCommand, relief='groove')
SettingLoadButton.place(relx=0.5, rely=0.9, relwidth=0.2, relheight=0.08, anchor=tk.CENTER)

def RunButtonCommand():
    seat = Seat.copy()
    member = MemberList.copy()
    cnt = 0
    r = int(RowSpinbox.get())
    c = int(ColumnSpinbox.get())
    for i in Seat:
        for j in i:
            cnt += 1 if (j == '.') else 0
    if (cnt > len(MemberList)):
        messagebox.showerror('인원수 부족', '자리수보다 인원수가 적습니다.')
        return
    elif (cnt < len(MemberList)):
        messagebox.showerror('인원수 과다', '자리수보다 인원수가 많습니다.')
        return
    rwin = tk.Tk()
    rwin.title('자리뽑기 결과')
    rwin.geometry(win.geometry())
    rwin.iconphoto(False, tk.PhotoImage(file='util/chair.png', master=rwin))
    SeatButton:list[list[tk.Button]] = []
    TableLabel = ttk.Label(rwin, text='교탁', borderwidth=1, relief='groove', anchor=tk.CENTER)
    TableLabel.place(relx=0.5, rely=0, anchor=tk.N, relwidth=0.4, relheight=0.9/(int(r)*2+1)/1.5)
    TitleLabel = ttk.Label(rwin, text='제목:', justify='center')
    TitleLabel.place(relx=0.79, rely=0, anchor=tk.N, relwidth=0.1, relheight=0.9/(int(r)*2+1)/1.5)
    TitleInput = ttk.Entry(rwin)
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    TitleInput.insert(tk.END, string=now.strftime("%Y-%m-%d-%H:%M:%S"))
    TitleInput.place(relx=0.85, rely=0, anchor=tk.N, relwidth=0.1, relheight=0.9/(int(r)*2+1)/1.5)
    for i in range(int(len(seat))):
        SeatButton.append([])
        for j in range(int(len(seat[i]))):
            b = tk.Button(rwin, text='-' if seat[i][j] == '.' else 'X', relief='groove', background='#c2f1f5' if seat[i][j] == '.' else '#f5c2c2')
            b.config(font=font.Font(family='Malgun Gothic', size=min(b.winfo_width(), b.winfo_height()), weight='bold'))
            SeatButton[i].append(b)
            b.place(relwidth=1/(int(c)*2),relheight=0.9/(int(r)*2+1),relx = (1/(int(c) + 1) * (j+1)), rely=(0.9 / (int(r)+1) * (i+1)), anchor=tk.CENTER)
    random.shuffle(member)
    class Member:
        def __init__(self, name:str, x:int, y:int):
            self.name = name
            self.x = x
            self.y = y
    arr:list[Member] = []
    for i in range(len(seat)):
        for j in range(len(seat[i])):
            if (seat[i][j] == '-'):
                continue
            arr.append(Member(member.pop(), i, j))
    random.shuffle(arr)
    def ShowButtonCommand(idx:int):
        if (idx == 0):
            ShowButton.config(state='disabled')
        if idx == len(arr):
            EditButton.config(state=tk.NORMAL)
            SaveStateButton.config(state=tk.NORMAL)
            return
        m = arr[idx]
        SeatButton[m.x][m.y].config(text=m.name, bg='#c2f5de', font=font.Font(family='맑은 고딕', weight='bold', size=min(SeatButton[m.x][m.y].winfo_width(), SeatButton[m.x][m.y].winfo_height())))
        rwin.after(100, ShowButtonCommand, idx + 1)
    
    CheckX = -1
    CheckY = -1
    def EditableButtonCommand(i, j):
        def innner():
            nonlocal CheckX, CheckY
            if (CheckX >= 0 and CheckY >= 0):
                t = SeatButton[CheckX][CheckY]['text']
                u = SeatButton[i][j]['text']
                SeatButton[CheckX][CheckY].config(text=u, relief=tk.GROOVE)
                SeatButton[i][j].config(text=t)
                CheckX = -1
                CheckY = -1
            else:
                SeatButton[i][j].config(relief=tk.SUNKEN)
                CheckX = i
                CheckY = j
        return innner
    def EditButtonCommand():
        if (EditButton['relief'] == 'groove'):
            EditButton.config(relief=tk.SUNKEN)
            for i in range(len(SeatButton)):
                for j in range(len(SeatButton[i])):
                    if (SeatButton[i][j]['bg'] == '#f5c2c2'):
                        continue
                    SeatButton[i][j].config(command=EditableButtonCommand(i, j))
        else:
            EditButton.config(relief=tk.GROOVE)
            for i in range(len(SeatButton)):
                for j in range(len(SeatButton[i])):
                    SeatButton[i][j].config(command=lambda : 0)

    def SaveStateButtonCommand():
        fn = filedialog.asksaveasfilename(initialdir='./result', filetypes=(('Seat Arrange Files', '*.saf'), ), title='Save State as', initialfile=now.strftime("%Y-%m-%d-%H-%M-%S"))
        if (not fn):
            return
        #fn = messagebox.askquestion('파일이름', '저장할 파일의 이름을 입력해주세요.')
        #if (not fn):
        #    return
        title = TitleInput.get()
        w = 1042
        h = 617
        objfont = ImageFont.truetype('malgunbd.ttf', 18, encoding='utf-8')
        img = Image.new('1', (w, h))
        img.paste(1, (0, 0, w, h))
        drawer = ImageDraw.Draw(img)
        drawer.rectangle((0, 0, w, h))
        drawer.rectangle(((3,3, 116,39)))#뒷문
        drawer.text((119/2, 42/2), '뒷문', anchor='mm', align='center', font=objfont)
        drawer.rectangle((117,3,1039, 39))#사물함
        drawer.text((1156/2, 42/2), '사물함', anchor='mm', align='center', font=objfont)
        cellw = (1036 - 2*(len(seat[0])-1))/ (12*len(seat[0])-1)*11
        cellh = 499 / len(seat) - 1
        voidw = (1036 - 2*(len(seat[0])-1))/ (12*len(seat[0])-1)
        h = 0
        maxlen = 0
        for i in arr:
            maxlen = max(maxlen, len(i.name))
        mfont = ImageFont.truetype('malgunbd.ttf', int(min((cellw)/maxlen, (cellh)/2)))
        for i in range(len(seat)):
            for j in range(len(seat[i])):
                drawer.rectangle((3+cellw*j+voidw*j+2*j, 40+i+cellh*i, 3+cellw*(j+1)+voidw*j+2*j, 40+i+cellh*(i+1)))#좌석
                text = SeatButton[r - i - 1][c - j - 1]['text']
                drawer.text(((3+cellw*j+voidw*j+2*j+3+cellw*(j+1)+voidw*j+2*j)/2, (40+i+cellh*i+40+i+cellh*(i+1))/2), text=text, anchor='mm', align='center', font=mfont)
                drawer.rectangle((4+cellw*(j+1)+voidw*j+2*j,40+i+cellh*i, 4+cellw*(j+1)+voidw*(j+1)+2*j,40+i+cellh*(i+1)))
                h = max(h, 40+i+cellh*(i+1))
        drawer.rectangle((3,h, 115,573))#앞문
        drawer.text((118/2,(h+573)/2), '앞문', font=objfont, anchor='mm', align='center')
        drawer.rectangle((116,h, 1039,573))#교탁
        drawer.text((1155/2, (h+573)/2), '교탁', font=objfont, anchor='mm', align='center')
        drawer.rectangle((3,h+34, 1039, 614))#제목
        drawer.text((1042/2, (h+648)/2), title, font=ImageFont.truetype('malgunbd.ttf', size=int(570-h)), anchor='mm', align='center')
        img.save(f'{fn}.jpg')
        f = open(f'{fn}.saf', 'w', encoding='utf-8')
        f.write(f'{len(SeatButton)} {len(SeatButton[0])}\n')
        for i in SeatButton:
            for j in i:
                if (j['text'] == 'X'):
                    f.write('- ')
                else:
                    f.write('. ')
            f.write('\n')
        for i in SeatButton:
            for j in i:
                if (j['text'] != 'X'):
                    f.write(j['text'] + '\n')
        img.show()
        f.close()
        
        


    def LoadStateButtonCommand():
        nonlocal SeatButton, TableLabel, seat, r, c, arr
        fn = filedialog.askopenfilename(initialdir='./loader', filetypes=(('Seat Arrange File', '*.saf'),), title='Open State as')
        f = open(fn, 'r', encoding='utf-8')
        r, c = f.readline().strip('\n').split()
        r = int(r)
        c = int(c)
        seat = []
        arr = []
        for i in range(r):
            seat.append(f.readline().strip('\n').split())
        for i in range(r):
            for j in range(c):
                if (seat[i][j] == '-'):
                    seat[i][j] = 'X'
                else:
                    seat[i][j] = f.readline().strip('\n')
                    arr.append(Member(seat[i][j], i, j))
        for i in SeatButton:
            for j in i:
                j.destroy()
        SeatButton = []
        TableLabel.destroy()
        TableLabel = ttk.Label(rwin, text='교탁', borderwidth=1, relief='groove', anchor=tk.CENTER).place(relx=0.5, rely=0, anchor=tk.N, relwidth=0.4, relheight=0.9/(int(r)*2+1)/1.5)
        for i in range(int(len(seat))):
            SeatButton.append([])
            for j in range(int(len(seat[i]))):
                b = tk.Button(rwin, text=seat[i][j], relief='groove', background='#c2f5de' if seat[i][j] != 'X' else '#f5c2c2')
                b.config(font=font.Font(family='맑은고딕', size=min(b.winfo_width(), b.winfo_height()), weight='bold'))
                SeatButton[i].append(b)
                b.place(relwidth=1/(int(c)*2),relheight=0.9/(int(r)*2+1),relx = (1/(int(c) + 1) * (j+1)), rely=(0.9 / (int(r)+1) * (i+1)), anchor=tk.CENTER)
        ShowButton['state'] = 'disabled'
        SaveStateButton['state'] = 'normal'
        EditButton['state'] = 'normal'
        f.close()
        
    EditButton = tk.Button(rwin, relief='groove', command=EditButtonCommand, text='수정', state='disabled')
    EditButton.place(relx=0.2, rely=0.9, relwidth=0.2, relheight=0.1, anchor=tk.CENTER)
    
    SaveStateButton = tk.Button(rwin, relief='groove', text='저장', command=SaveStateButtonCommand, state='disabled')
    SaveStateButton.place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.1, anchor=tk.CENTER)

    LoadStateButton = tk.Button(rwin, relief='groove', text='불러오기', command=LoadStateButtonCommand)
    LoadStateButton.place(relx=0.55, rely=0.9, relwidth=0.1, relheight=0.1, anchor=tk.CENTER)

    ShowButton = tk.Button(rwin, relief='groove', command=lambda : ShowButtonCommand(0), text='공개')
    ShowButton.place(relx=0.8, rely=0.9, relwidth=0.2, relheight=0.1, anchor=tk.CENTER)
    


    rwin.focus_force()
    rwin.mainloop()



RunButton = tk.Button(win, text='완료', command=RunButtonCommand, relief='groove')
RunButton.place(relx=0.8, rely=0.9, relwidth=0.2, relheight=0.08, anchor=tk.CENTER)



SettingLabelFrame.place(relwidth=0.9, relheight=0.2, relx=0.5, rely=0.1, anchor=tk.CENTER)
#SettingLabelFrame.pack(fill='x', side='top', pady=20, padx=20, ipadx=20)
SeatLabelFrame.place(relwidth=0.9, relheight=0.65, relx=0.5, rely=0.2, anchor=tk.N)
#SeatLabelFrame.pack(fill='x', expand=1, pady=10)

win.mainloop()