from tkinter import *
from tkinter.ttk import Treeview
import time
import cx_Oracle as Cx
import welcomepage
import studenthomepage


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


def addNewAdmin(root):
    root.destroy()
    root = Tk()
    root.geometry('500x500')
    root.resizable(FALSE, FALSE)
    root.title('Add New Admin')
    Label(root, text="Admin Registration form", width=20, fg='red', font=("bold", 20)).place(x=90, y=53)

    label_1 = Label(root, text="User ID", width=20, font=("bold", 10))
    label_1.place(x=80, y=130)
    entry_1 = Entry(root)
    entry_1.place(x=240, y=130)
    label_2 = Label(root, text="Name", width=20, font=("bold", 10))
    label_2.place(x=75, y=180)
    entry_2 = Entry(root)
    entry_2.place(x=240, y=180)
    label_3 = Label(root, text="Password", width=20, font=("bold", 10))
    label_3.place(x=68, y=230)
    entry_3 = Entry(root, show='*')
    entry_3.place(x=240, y=230)

    Button(root, text='Submit', width=20, bg='brown', fg='white',
           command=lambda: addAdmin(root, entry_1.get(), entry_2.get(), entry_3.get())).place(x=120, y=380)
    Button(root, text='Go Back', width=20, bg='brown', fg='white', command=lambda: adminWelcomePage(root)).place(x=280,
                                                                                                                 y=380)


def approveStudent(root, sid):
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    selectStmt = 'select * from pending_req where userid= \'' + sid + '\''
    cur.execute(selectStmt)
    print(selectStmt)
    rs = cur.fetchall()
    if (len(rs) == 0):
        Label(root, text=sid + ' was not authorized', fg='red', font=('bold', 15)).place(x=450, y=650)
    else:
        sid = rs[0][0]
        uname = rs[0][1]
        pwd = rs[0][2]
        vj = rs[0][3]
        cf = rs[0][4]
        insertStmt = 'insert into user_info values(\'' + sid + '\',\'' + uname + '\',\'' + pwd + '\',0)'  # + vj + '\',\'' + cf + '\')'
        insertStmt2 = 'insert into handle_info values(\'' + sid + '\',\'' + cf + '\',\'' + vj + '\',2)'
        print(insertStmt2)
        print(insertStmt)
        cur.execute(insertStmt)
        conn.commit()
        cur.execute(insertStmt2)
        conn.commit()
        cur.execute('delete from pending_req where userid = \'' + sid + '\'')
        conn.commit()
        Label(root, text=sid + ' was authorized', fg='red', font=('bold', 15)).place(x=450, y=650)
        conn.close()
        Label(root, text=' wait for 3 second', fg='red', font=('bold', 15)).place(x=450, y=700)
        approvePendingRequest(root)


def approvePendingRequest(root):
    root.destroy()
    root = Tk()
    root.title('pending request')
    root.geometry('1200x750')
    root.resizable(FALSE, FALSE)
    Label(root, text='Pending Approval', fg='red', font=('bold', 20)).place(x=470, y=100)
    entry1 = Entry(root, width=40)
    b1 = Button(root, text='Authorize', fg='red', width=20, command=lambda: approveStudent(root, entry1.get()))
    b2 = Button(root, text='Go Back', fg='red', width=20, command=lambda: adminWelcomePage(root))
    entry1.place(x=350, y=140)
    b1.place(x=600, y=140)
    b2.place(x=750, y=140)
    tv = Treeview(root, columns=(1, 2, 3, 4), show="headings", height='20')
    tv.heading(1, text='Student ID')
    tv.heading(2, text='Name')
    tv.heading(3, text='Vjudge Handle')
    tv.heading(4, text='Codeforces Handle')
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
        tv.insert("", "end", values=(sid, un, vj, cf))
    tv.place(x=180, y=180)


def adminWelcomePage(root):
    root.destroy()
    root = Tk()
    root.geometry('1250x790')
    Label(root, text='Welcome to IUTPC Rating System', fg='red', font=('bold', 20)).place(x=440, y=50)
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    Button(root, text='Add Contest', width=20, height=5, fg='red', borderwidth=3).place(x=180, y=250)
    Button(root, text='Previous Contest', width=20, height=5, fg='red', borderwidth=3).place(x=335, y=250)
    Button(root, text='Student Ranking', width=20, height=5, fg='red', borderwidth=3).place(x=490, y=250)
    Button(root, text='Pending Join Request', width=20, height=5, fg='red', borderwidth=3,
           command=lambda: approvePendingRequest(root)).place(x=645, y=250)
    Button(root, text='Add New Admin', width=20, height=5, fg='red', borderwidth=3,
           command=lambda: addNewAdmin(root)).place(x=800, y=250)
    Button(root, text='Logout', width=20, height=5, bg='grey', fg='red', borderwidth=3,
           command=lambda: welcomepage.startpage(root)).place(x=955, y=250)
    root.mainloop()
    return


if __name__ == "__main__":
    root = Tk()
    adminWelcomePage(root)
    root.mainloop()
