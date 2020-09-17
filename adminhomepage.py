from tkinter import *
from tkinter.ttk import Treeview
import cx_Oracle as Cx
import welcomepage
import RatingFetcherFromCodeforces
import VerifyAndAddContest
import tkinter.font as fonts
import tkinter.ttk as ttk

# Pranon
def addAdmin(root, uid, uname, pwd):
    new = Tk()
    new.geometry('250x250')
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    stmt = 'insert into user_info values ( \'' + uid + '\',\'' + uname + '\',\'' + pwd + '\', 1)'
    try:
        cur.execute(stmt)
    except Cx.IntegrityError:
        Label(new, text='Try different Username').place(x=80, y=50)
        addNewAdmin(root)
    else:
        Label(new, text='New Admin Added').place(x=80, y=50)
        addNewAdmin(root)
    conn.commit()
    print(stmt)
    conn.close()


# RIZVI
def addNewAdmin(root):
    root.destroy()
    root = Tk()
    root.geometry('500x450')
    root.resizable(FALSE, FALSE)
    root.title('Add New Admin')
    myFont = fonts.Font(family='Georgia',size=16)
    headerFont = fonts.Font(family='Century Schoolbook',size=20)
    Label(root, text="Admin Registration form", width=20, fg='red', font=headerFont).place(x=90, y=53)

    label_1 = Label(root, text="User ID", width=20, font=myFont)
    label_1.place(x=0, y=150)
    entry_1 = Entry(root, font=myFont,width=20)
    entry_1.place(x=170, y=150)
    label_2 = Label(root, text="Name", width=20, font=myFont)
    label_2.place(x=5, y=190)
    entry_2 = Entry(root, font=myFont,width=20)
    entry_2.place(x=170, y=190 )
    label_3 = Label(root, text="Password", width=20, font=myFont, justify = CENTER)
    label_3.place(x=-5, y=230)
    entry_3 = Entry(root, show='*', font=myFont,width=20)
    entry_3.place(x=170, y=230)

    Button(root, text='Submit', width=10, bg='brown', fg='white', font= myFont, padx=0, pady=0, justify=CENTER,
           command=lambda: addAdmin(root, entry_1.get(), entry_2.get(), entry_3.get())).place(x=120, y=300)
    Button(root, text='Go Back', width=10, bg='black', fg='white', font= myFont, padx=0, pady=0, justify=CENTER,
           command=lambda: adminWelcomePage(root)).place(x=280, y=300)


# PRANON
def approveStudent(root, sid, flag):
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    if flag != 1:
        selectStmt = 'select * from pending_req where userid= \'' + sid + '\''
        cur.execute(selectStmt)
        print(selectStmt)
        rs = cur.fetchall()
        if len(rs) == 0:
            Label(root, text=sid + ' was not authorized', fg='red', font=('bold', 15)).place(x=450, y=650)
        else:
            sid = rs[0][0]
            uname = rs[0][1]
            pwd = rs[0][2]
            vj = rs[0][3]
            cf = rs[0][4]
            toph = rs[0][5]
            insertStmt = 'insert into user_info values(\'' + sid + '\',\'' + uname + '\',\'' + pwd + '\',0)'
            insertStmt2 = 'insert into handle_info values(\'' + sid + '\',\'' + cf + '\',\'' + vj + '\' , \'' + toph + '\',2)'
            print(insertStmt2)
            print(insertStmt)
            rating = RatingFetcherFromCodeforces.cfRating(cf)
            insertStmt3 = 'insert into current_rating values(\'' + sid + '\', ' + str(rating) + ' , ' + str(
                'NULL') + ' , ' + str(rating) + ')'
            cur.execute(insertStmt)
            conn.commit()
            cur.execute(insertStmt2)
            conn.commit()
            cur.execute(insertStmt3)
            conn.commit()
            cur.execute('delete from pending_req where userid = \'' + sid + '\'')
            conn.commit()
            Label(root, text=sid + ' was authorized', fg='red', font=('bold', 15)).place(x=450, y=650)
            conn.close()
            Label(root, text=' wait for 3 second', fg='red', font=('bold', 15)).place(x=450, y=700)

    else:
        cur.execute('delete from pending_req where userid = \'' + sid + '\'')
        conn.commit()
        Label(root, text=sid + ' was deleted', fg='red', font='bold,15').place(x=450, y=650)
    approvePendingRequest(root)


# RIZVI
def approvePendingRequest(root):
    root.destroy()
    root = Tk()
    root.title('pending request')
    root.geometry('1200x750')
    root.resizable(FALSE, FALSE)

    myFont = fonts.Font(family='Georgia',size=14)
    headerFont = fonts.Font(family='Century Schoolbook',size=26)
    insertFont = fonts.Font(family='Century Schoolbook',size=9)


    Label(root, text='Pending Approval', fg='red', font=(headerFont)).place(x=470, y=50)
    entry1 = Entry(root, width=28 ,font = myFont, justify=CENTER, border=3)
    b1 = Button(root, text='Authorize', fg='red', bg='#c7c7c7', width=20, font = myFont, padx=0, pady=0, justify=CENTER,
                command=lambda: approveStudent(root, entry1.get(), 0))
    b2 = Button(root, text='Go Back', fg='white', bg='black', width=30, font= myFont, padx=0, pady=0, justify=CENTER,
                command=lambda: adminWelcomePage(root))
    b3 = Button(root, text='Delete Request', fg='black', bg='#c7c7c7', width=20, font= myFont, padx=0, pady=0, justify=CENTER,
                command=lambda: approveStudent(root, entry1.get(), 1))
    entry1.place(x=220, y=130)
    b1.place(x=590, y=125)
    b2.place(x=450, y=650)
    b3.place(x=830, y=125)
    tv = Treeview(root, columns=(1, 2, 3, 4, 5), show="headings", height='12')

    style = ttk.Style()
    style.configure("Treeview", font=myFont, rowheight=30, bg ='#c6c6c6', relief='flat')
    style.configure("Treeview.Heading", font=insertFont, bg='#c6c6c6')

    tv.heading(1, text='Student ID')
    tv.heading(2, text='Name')
    tv.heading(3, text='Vjudge Handle')
    tv.heading(4, text='Codeforces Handle')
    tv.heading(5, text='Toph Handle')
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    stmt = 'select * from pending_req'
    cur.execute(stmt)
    rs = cur.fetchall()
    for row in rs:
        sid = row[0]
        un = row[1]
        vj = row[3]
        cf = row[4]
        toph = row[5]
        tv.insert("", "end", values=(sid, un, vj, cf, toph), tags=("red"))
    tv.place(x=110, y=200)


# RIZVI
def showAllStudentRanking(root):
    root.destroy()
    root = Tk()
    root.geometry('1250x790')
    myFont = fonts.Font(family='Georgia',size=14)
    headerFont = fonts.Font(family='Century Schoolbook',size=30)
    insertFont = fonts.Font(family='Century Schoolbook',size=9)

    Label(root, text='Student Rating (Descending Order)', fg='red', font=headerFont).place(x=320, y=50)
    tv = Treeview(root, columns=(1, 2, 3, 4), show="headings", height='15')

    style = ttk.Style()
    style.configure("Treeview", font=myFont, rowheight=30, bg ='#c6c6c6', relief='flat')
    style.configure("Treeview.Heading", font=insertFont, bg='#c6c6c6')

    tv.heading(1, text='Rank Number')
    tv.heading(2, text='Student ID')
    tv.heading(3, text='Codeforces Rating')
    tv.heading(4, text='Overall Rating')
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    stmt = 'select userid,cf_rating, OVERALL_RATING from current_rating order by overall_rating desc'
    cur.execute(stmt)
    rs = cur.fetchall()
    curr = 1
    for row in rs:
        sid = curr
        un = row[0]
        vj = row[1]
        cf = row[2]
        tv.insert("", "end", values=(sid, un, vj, cf))
        curr += 1
    tv.place(x=240, y=180)
    Button(root, text='Go Back', fg='white', bg='black', width=20, font=myFont, command=lambda: adminWelcomePage(root)).place(x=515, y=720)


# PRANON
def verifyNewCon(root, name, url, plat, div, man):
    root.destroy()
    p = VerifyAndAddContest.getContestStatus(name, url, plat, div, man)
    # adminWelcomePage(root)


# RIZVI
def addNewContest(root):
    root.destroy()
    root = Tk()
    root.geometry('500x500')
    root.resizable(FALSE, FALSE)
    myFont = fonts.Font(family='Georgia',size=16)
    headerFont = fonts.Font(family='Century Schoolbook',size=26)
    root.title("Add New Contest")
    label_0 = Label(root, text="Add New Contest", width=20, fg='Red', font=("bold", 20))
    label_0.place(x=90, y=53)

    label_1 = Label(root, text="Contest Name: ", width=20, font=("bold", 10))
    label_1.place(x=80, y=130)
    entry_1 = Entry(root, width=40)
    entry_1.place(x=210, y=130)

    label_2 = Label(root, text="Contest URL: ", width=20, font=("bold", 10))
    label_2.place(x=80, y=180)
    entry_2 = Entry(root, width=40)
    entry_2.place(x=210, y=180)

    platform = StringVar()
    Label(root, text='Platform:', width=20, font=('bold', 10)).place(x=63, y=210)
    Radiobutton(root, text='codeforces', variable=platform, value='codeforces').place(x=120, y=230)
    Radiobutton(root, text='vjudge', variable=platform, value='vjudge').place(x=120, y=250)
    Radiobutton(root, text='toph', variable=platform, value='toph').place(x=120, y=270)

    div = IntVar()
    Label(root, text='Division:', width=20, font=('bold', 10)).place(x=63, y=290)
    Radiobutton(root, text='Div 1+2', variable=div, value=0).place(x=120, y=310)
    Radiobutton(root, text='Div 1', variable=div, value=1).place(x=120, y=330)
    Radiobutton(root, text='Div 2', variable=div, value=2).place(x=120, y=350)

    man = IntVar()
    Label(root, text='Mandatory:', width=20, font=('bold', 10)).place(x=63, y=370)
    Radiobutton(root, text='Yes', variable=man, value=0).place(x=120, y=390)
    Radiobutton(root, text='No ', variable=man, value=1).place(x=120, y=410)

    Button(root, text='Fetch Result for Contest', fg='red', bg='grey',
           command=lambda: verifyNewCon(root, entry_1.get(), entry_2.get(), platform.get(), div.get(),
                                        man.get())).place(x=240, y=460)


# RIZVI
def showRanklist(root, cid):
    root.destroy()
    root = Tk()
    root.geometry('1400x790')
    myFont = fonts.Font(family='Georgia',size=16)
    headerFont = fonts.Font(family='Century Schoolbook',size=26)
    root.title('Contest Ranklist')
    Label(root, text='Contest Ranklist', fg='red', font=('bold', 20)).place(x=440, y=50)
    tv = Treeview(root, columns=(1, 2, 3, 4, 5), show="headings", height='20')
    tv.heading(1, text='Position')
    tv.heading(2, text='Student ID')
    tv.heading(3, text='Solved')
    tv.heading(4, text='Time Penalty')
    tv.heading(5, text='Rating Change')

    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    stmt = 'select userid, point_gained, time_penalty,change_rating  from ranklist where contest_id = \'' + cid + '\''
    cur.execute(stmt)
    rs = cur.fetchall()
    curr = 1
    ranklist = []
    for row in rs:
        un = row[0]
        vj = row[1]
        cf = row[2]
        rj = row[3]
        ranklist.append((curr, un, vj, cf, rj))
    ranklist.sort(key=lambda x: (x[2], -x[3]), reverse=True)
    for item in ranklist:
        un = item[1]
        vj = item[2]
        cf = item[3]
        rj = item[4]
        tv.insert("", "end", values=(curr, un, vj, cf, rj))
        curr += 1
    tv.place(x=240, y=180)
    Button(root, text='Go Back', fg='red', width=20, command=lambda: adminWelcomePage(root)).place(x=540, y=720)

    root.mainloop()


# RIZVI
def showPreviousContest(root):
    root.destroy()
    root = Tk()
    root.geometry('1200x790')
    myFont = fonts.Font(family='Georgia',size=16)
    headerFont = fonts.Font(family='Century Schoolbook',size=26)
    root.title('Previous Contest')
    Label(root, text='Previous Contest', fg='red', font=('bold', 20)).place(x=440, y=50)
    entry1 = Entry(root, width=50)
    b1 = Button(root, text='Show Ranklist', fg='red', width=20, command=lambda: showRanklist(root, entry1.get()))
    entry1.place(x=250, y=140)
    b1.place(x=550, y=140)
    tv = Treeview(root, columns=(1, 2, 3), show="headings", height='20')
    tv.heading(1, text='Contest ID')
    tv.heading(2, text='Contest Name')
    tv.heading(3, text='Contest URL')
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    stmt = 'select contest_id,contest_name,contest_url from contest_info'
    cur.execute(stmt)
    rs = cur.fetchall()
    curr = 1
    for row in rs:
        un = row[0]
        vj = row[1]
        cf = row[2]
        tv.insert("", "end", values=(un, vj, cf))
    tv.place(x=240, y=180)
    Button(root, text='Go Back', fg='red', width=20, command=lambda: adminWelcomePage(root)).place(x=540, y=720)

    root.mainloop()


# RIZVI
def adminWelcomePage(root):
    root.destroy()
    root = Tk()
    myFont = fonts.Font(family='Georgia',size=16)
    headerFont = fonts.Font(family='Century Schoolbook',size=26)
    root.geometry('850x780')
    Label(root, text='Welcome to IUTPC Rating System', fg='red', font=(headerFont)).place(x=158, y=50)
    Button(root, text='Add Contest', width=40, height=2, fg='red', bg='#c7c7c7', borderwidth=5,font=myFont, padx=0, pady=0, justify = CENTER,
           command=lambda: addNewContest(root)).place(x=180, y=150)
    Button(root, text='Previous Contest', width=40, height=2, fg='red', bg='#c7c7c7', borderwidth=5,font=(myFont), padx=0, pady=0, justify = CENTER,
           command=lambda: showPreviousContest(root)).place(x=180, y=250)
    Button(root, text='Student Ranking', width=40, height=2, fg='red', bg='#c7c7c7', borderwidth=5,font=(myFont), padx=0, pady=0, justify = CENTER,
           command=lambda: showAllStudentRanking(root)).place(x=180, y=350)
    Button(root, text='Pending Join Request', width=40, height=2, fg='red',bg='#c7c7c7', borderwidth=5,font=(myFont), padx=0, pady=0, justify = CENTER,
           command=lambda: approvePendingRequest(root)).place(x=180, y=450)
    Button(root, text='Add New Admin', width=40, height=2, fg='red',bg='#c7c7c7', borderwidth=5,font=(myFont), padx=0, pady=0, justify = CENTER,
           command=lambda: addNewAdmin(root)).place(x=180, y=550)
    Button(root, text='Logout', width=40, height=2, fg='white',bg='black', borderwidth=5,font=(myFont), padx=0, pady=0, justify = CENTER,
           command=lambda: welcomepage.startpage(root)).place(x=180, y=650)
    root.mainloop()
    return


if __name__ == "__main__":
    root = Tk()
    adminWelcomePage(root)
    root.mainloop()
