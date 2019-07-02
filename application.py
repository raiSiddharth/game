import csv
from flask import Flask, render_template, session, redirect, url_for, request
from flask_session import Session
from tempfile import mkdtemp
import random

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def check(li, f, ch):
    flag=f

    #horizontal checking
    for i in range (3):
        co=0
        for j in range (3):
            if li[i][j]==ch:
                co+=1
        if co==2 and flag==0:
            for k in range (3):
                if li[i][k]==None:
                    li[i][k]="O"
                    flag=1
                    check(li,flag,ch)
                    return 1
        if co==3:
            winner=ch
            return ch

    #vertical checking
    for i in range (3):
        c1=0
        for j in range (3):
            if li[j][i]==ch:
                c1+=1
        if c1==2 and flag==0:
            for k in range (3):
                if li[k][i]==None:
                    li[k][i]="O"
                    flag=1;
                    check(li,flag,ch)
                    return 1
        if c1==3:
            winner=ch
            return ch

    #diagonal checking
    c3=0
    for i in range(3):
        if li[i][i]==ch:
            c3+=1
            a=i
            b=i
    if c3==2  and flag==0:
        for k in range (3):
            if li[k][k]==None:
                li[k][k]="O"
                flag=1;
                check(li,flag,ch)
                return 1
    if c3==3:
        winner=ch
        return ch

    #diagonal 2 checking
    j=2
    c4=0
    for i in range (3):
        if li[i][j]==ch:
            c4+=1
            a=i
            b=j
        j-=1
    if c4==2 and flag==0:
        j=2
        for k in range (3):
            if li[k][j]==None:
                li[k][j]="O"
                flag=1;
                check(li,flag,ch)
                return 1
            j-=1
    if c4==3:
        winner=ch
        return ch

    #Counter over. Code for game play
    if flag==0 and ch=="O":
        if (c3==1 or c4==1) and li[2-a][2-b]==None:
            li[2-a][2-b]="O"
            flag=1
            return

    #to return to counter O, to first counter from 2nd counter
    if flag==0 and ch=="X":
        return 0

    #to send to counter X
    if flag==0 and ch=="O":
        flag=check(li,flag,"X")

    #sanity check
    if flag==4 and ch=="O":
        flag=check(li,flag,"X")

    if flag=="O" or flag=="X":
        return flag

    if flag==0:
        for i in range(0,3,2):
            for j in range(0,3,2):
                if li[i][j]==None:
                    li[i][j]="O"
                    flag=1
                    fn=check(li,flag,"O")
                    return fn
    if flag==0:
        for i in range(3):
            for j in range(3):
                if li[i][j]==None:
                    li[i][j]="O"
    #DRAW
    flag1=0
    for i in range(3):
        for j in range(3):
            if li[i][j]==None:
                flag1=1
    if flag1==0:
        return 3

global score_comp, score_player, username
score_comp=0
score_player=0
@app.route("/", methods=["GET", "POST"])
def index():


    if request.method == "GET":
        return render_template("index.html")

    else:
        username=request.form.get("username")

        with open("users.csv", mode="a") as users_file:
            users = csv.writer(users_file)
            users.writerow(username)

        if "board" not in session:
            score_comp=0
            score_player=0
            session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
            session["turn"] = "X"
            session["username"]=username
            a=random.randrange(0,3,2)
            b=random.randrange(0,3,2)
            session["board"][a][b]="O"

        return redirect("/start")



@app.route("/start")
def start():


    return render_template("game.html", game=session["board"],username=session["username"], sc=score_comp,su=score_player)

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    fl=0
    global score_comp
    global score_player
    session["board"][row][col]="X"
    fl=check(session["board"],0,"O")

    #this is just to check for winner
    fl=check(session["board"],4,"O")

    if fl=="O":
        score_comp+=1
        return render_template("win.html", game=session["board"], winner="Siddharth", sc=score_comp,su=score_player)
    elif fl=="X":
        score_player+=1
        return render_template("win.html", game=session["board"], winner=session["username"], sc=score_comp,su=score_player)
    elif fl==3:
        return render_template("draw.html", game=session["board"], sc=score_comp,su=score_player,username=session["username"])
    else:
        return render_template("game.html", game=session["board"], sc=score_comp,su=score_player,username=session["username"])

@app.route("/reset")
def reset():
    session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
    session["turn"] = "X"
    a=random.randrange(0,3,2)
    b=random.randrange(0,3,2)
    session["board"][a][b]="O"

    return render_template("game.html", game=session["board"],sc=score_comp,su=score_player)
