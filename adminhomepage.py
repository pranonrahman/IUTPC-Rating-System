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
    root.geometry('500x580')
    root.resizable(FALSE, FALSE)

    myFont = fonts.Font(family='Georgia', size=14)
    headerFont = fonts.Font(family='Century Schoolbook', size=26)

    root.title("Add New Contest")

    label_0 = Label(root, text="Add New Contest", width=20, fg='Red', font=(headerFont))
    label_0.place(x=40, y=53)

    label_1 = Label(root, text="Contest Name: ", width=20, font=(myFont))
    label_1.place(x=-25, y=130)
    entry_1 = Entry(root, width=25, font = myFont, border=3)
    entry_1.place(x=150, y=130)

    label_2 = Label(root, text="Contest URL: ", width=20, font=(myFont))
    label_2.place(x=-20, y=180)
    entry_2 = Entry(root, width=25, font=myFont, border=3)
    entry_2.place(x=150, y=180)

    platform = StringVar()
    Label(root, text='Platform:', width=20, font=myFont).place(x=-10, y=230)
    Radiobutton(root, text='codeforces', variable=platform, value='codeforces', font=myFont).place(x=70, y=260)
    Radiobutton(root, text='vjudge', variable=platform, value='vjudge', font=myFont).place(x=70, y=290)
    Radiobutton(root, text='toph', variable=platform, value='toph', font=myFont).place(x=70, y=320)

    div = IntVar()
    Label(root, text='Division:', width=20, font=myFont).place(x=200, y=230)
    Radiobutton(root, text='Div 1+2', variable=div, value=0, font=myFont).place(x=280, y=260)
    Radiobutton(root, text='Div 1', variable=div, value=1, font=myFont).place(x=280, y=290)
    Radiobutton(root, text='Div 2', variable=div, value=2, font=myFont).place(x=280, y=320)

    man = IntVar()
    Label(root, text='Mandatory:', width=20, font=myFont).place(x=-10, y=350)
    Radiobutton(root, text='Yes', variable=man, value=0, font=myFont).place(x=70, y=380)
    Radiobutton(root, text='No ', variable=man, value=1, font=myFont).place(x=70, y=410)

    fetchResultButton = Button(root, text='Fetch Result for Contest', fg='red', bg='grey',  font=myFont,
           command=lambda: verifyNewCon(root, entry_1.get(), entry_2.get(), platform.get(), div.get(),
                                        man.get()))
    goBackButton = Button(root, text='Go Back', fg='white', bg='black', font=myFont,
           command=lambda: adminWelcomePage(root))
    fetchResultButton.place(x=80, y=480)
    goBackButton.place(x=320, y=480)


# RIZVI
def showRanklist(root, cid):
    root.destroy()
    root = Tk()
    root.geometry('1400x790')
    myFont = fonts.Font(family='Georgia', size=16)
    headerFont = fonts.Font(family='Century Schoolbook', size=30)
    insertFont = fonts.Font(family='Century Schoolbook', size=12)
    root.title('Contest Ranklist')
    Label(root, text='Contest Ranklist', fg='red', font=headerFont).place(x=500, y=50)

    tv = Treeview(root, columns=(1, 2, 3, 4, 5), show="headings", height='15')

    style = ttk.Style()
    style.configure("Treeview", font=insertFont, rowheight=30, bg='#c6c6c6', relief='flat', width=80)
    style.configure("Treeview.Heading", font=myFont, bg='#c6c6c6')

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
    tv.place(x=200, y=180)
    Button(root, text='Go Back', fg='white', bg='black', width=20, font=myFont,
           command=lambda: showPreviousContest(root)).place(x=540, y=700)

    root.mainloop()


# RIZVI
def showPreviousContest(root):
    root.destroy()
    root = Tk()
    root.geometry('860x790')
    myFont = fonts.Font(family='Georgia',size=16)
    headerFont = fonts.Font(family='Century Schoolbook',size=26)
    insertFont = fonts.Font(family='Century Schoolbook', size=12)
    root.title('Previous Contest')
    Label(root, text='Previous Contest', fg='red', font=headerFont).place(x=320, y=50)
    entry1 = Entry(root, width=20, font=myFont, border=5, justify=CENTER)
    b1 = Button(root, text='Show Ranklist', fg='red', bg='#c6c6c6',width=13, font=myFont, border=5,
                command=lambda: showRanklist(root, entry1.get()))
    entry1.place(x=190, y=140)
    b1.place(x=480, y=133)

    tv = Treeview(root, columns=(1, 2, 3), show="headings", height=15)

    style = ttk.Style()
    style.configure("Treeview", font=insertFont, rowheight=30, bg='#c6c6c6', relief='flat',width=80)
    style.configure("Treeview.Heading", font=myFont, bg='#c6c6c6')

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
        vj = row[2]
        cf = row[1]
        tv.insert("", "end", values=(un, vj, cf))
    tv.place(x=120, y=200)
    Button(root, text='Go Back', fg='white', bg='black', width=30, font=myFont,
           command=lambda: adminWelcomePage(root)).place(x=240, y=720)

    root.mainloop()


def ShowStudentDetails(root):
    root.destroy()
    root = Tk()
    myFont = fonts.Font(family='Georgia', size=16)
    headerFont = fonts.Font(family='Century Schoolbook', size=30)
    insertFont = fonts.Font(family='Century Schoolbook', size=12)
    root.title('Student List')
    root.geometry('1200x750')
    root.resizable(FALSE, FALSE)
    Label(root, text='Student List', fg='red', font=headerFont).place(x=475, y=70)
    b2 = Button(root, text='Go Back', fg='white', bg='black', width=20, font=myFont,
                command=lambda: adminWelcomePage(root))
    b2.place(x=460, y=680)

    tv = Treeview(root, columns=(1, 2, 3, 4, 5), show="headings", height='15')

    style = ttk.Style()
    style.configure("Treeview", font=insertFont, rowheight=30, bg='#c6c6c6', relief='flat', width=80)
    style.configure("Treeview.Heading", font=myFont, bg='#c6c6c6')

    tv.heading(1, text='Student ID')
    tv.heading(2, text='Name')
    tv.heading(3, text='Vjudge Handle')
    tv.heading(4, text='Codeforces Handle')
    tv.heading(5, text='Rating')
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    stmt = 'select user_info.userid,user_info.name, handle_info.vjudge_handle, handle_info.cf_handle, current_rating.overall_rating from user_info, handle_info,current_rating where user_info.adminaccess=0 and user_info.userid = handle_info.userid and current_rating.userid = user_info.userid order by current_rating.overall_rating desc'
    cur.execute(stmt)
    rs = cur.fetchall()
    for row in rs:
        SID = row[0]
        un = row[1]
        vj = row[2]
        cf = row[3]
        rat = row[4]
        tv.insert("", "end", values=(SID, un, vj, cf, rat))
    tv.place(x=100, y=160)
    return


# RIZVI
def adminWelcomePage(root):
    root.destroy()
    root = Tk()
    myFont = fonts.Font(family='Georgia',size=16)
    headerFont = fonts.Font(family='Century Schoolbook',size=26)
    root.geometry('850x880')
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
    Button(root, text='See Student Details', width=40, height=2, fg='red',bg='#c7c7c7', borderwidth=5, font=(myFont), padx=0,
           pady=0, justify=CENTER,
           command=lambda: welcomepage.ShowStudentDetails(root)).place(x=180, y=650)
    Button(root, text='Logout', width=40, height=2,  borderwidth=5,font=(myFont), fg='white', bg='black', padx=0, pady=0, justify = CENTER,
           command=lambda: welcomepage.startpage(root)).place(x=180, y=750)
    root.mainloop()
    return


if __name__ == "__main__":
    root = Tk()
    adminWelcomePage(root)
    root.mainloop()
