from hashlib import new

import cx_Oracle as Cx
from tkinter import *
from adminhomepage import *
from studenthomepage import *
import RatingFetcherFromCodeforces
import tkinter.font as fonts


def click(new):
    new.destroy()
    return


def doRegistration(root, sid, name, pwd, vj, cf, toph):
    print(sid, name, pwd, vj, cf)
    myFont = fonts.Font(family='Georgia', size=16)
    headerFont = fonts.Font(family='Century Schoolbook', size=30)
    insertFont = fonts.Font(family='Century Schoolbook', size=12)
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    stmt = 'select userid from user_info where userid= \'' + sid + '\''
    cur.execute(stmt)
    rs = cur.fetchall()
    root.resizable(FALSE, FALSE)
    if len(rs) == 0:
        Label(root, text='Adding to database').place(x=240, y=420)
        stmt = 'insert into pending_req values(\'' + sid + '\',\'' + name + '\',\'' + pwd + '\',\'' + vj + '\',\'' + cf + '\' , \'' + toph + '\')'
        print(stmt)
        rating = RatingFetcherFromCodeforces.cfRating(cf)
        if rating == -1:
            MessageBox = Tk()
            MessageBox.geometry('500x500')
            MessageBox.resizable(FALSE, FALSE)
            MessageBox.title("Error Box")
            Label(MessageBox, text='Provide CF Handle Properly',font=myFont, fg='red').place(x=120, y=240)
            startpage(root)
        else:
            try:
                cur.execute(stmt)
            except Cx.IntegrityError:
                MessageBox = Tk()
                MessageBox.geometry('500x500')
                MessageBox.resizable(FALSE, FALSE)
                MessageBox.title("Error Box")
                Label(MessageBox, text='You have already registered',font=myFont, fg='red').place(x=120, y=200)
                startpage(root)
            else:
                conn.commit()
                MessageBox = Tk()
                MessageBox.geometry('500x500')
                MessageBox.resizable(FALSE, FALSE)
                MessageBox.title("Error Box")
                Label(MessageBox, text='Added Properly', font=myFont).place(x=180, y=240)
                startpage(root)
    else:
        print('already have this!')
        MessageBox = Tk()
        MessageBox.geometry('500x500')
        MessageBox.resizable(FALSE, FALSE)
        MessageBox.title("Error Box")
        Label(MessageBox, text='You are already registered into the system',font=myFont, fg='red').place(x=60, y=200)
        startpage(root)


def login(root, sid, pwd):
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    stmt = 'select password,adminaccess from user_info where userid = \'' + sid + '\''
    cur.execute(stmt)
    rs = cur.fetchall()
    new = Tk()
    new.geometry('400x400')
    new.destroy()
    root.resizable(FALSE, FALSE)
    if len(rs) != 0:
        if rs[0][0] == pwd:
            Label(root, text='Logged In').place(x=80, y=50)
            if rs[0][1] == 1:
                adminWelcomePage(root)
            else:
                studentWelcomePage(root, sid)

        else:
            neo = Tk()
            neo.geometry('200x200')
            Label(neo, text='Wrong Password').place(x=80, y=50)
            Button(neo, text='Go Back', width=20, bg='brown', fg='white', command=lambda: click(neo)).place(x=80, y=90)
            neo.mainloop()
            startpage(root)
    else:
        stmt = 'select password from pending_req where userid = \'' + sid + '\''
        cur.execute(stmt)
        rs = cur.fetchall()
        if len(rs) != 0:
            Label(root, text='Your account needs approval, ask your admin').place(x=80, y=50)
            root.destroy()
            startpage(root)
        else:
            Label(new, text='You are not registered, register first').place(x=80, y=50)
            new.destroy()
            startpage(root)
    new.mainloop()


def registration(root):
    root.destroy()
    root = Tk()
    root.geometry('500x530')
    root.resizable(FALSE, FALSE)
    myFont = fonts.Font(family='Georgia', size=16)
    headerFont = fonts.Font(family='Century Schoolbook', size=30)
    insertFont = fonts.Font(family='Century Schoolbook', size=12)
    root.title("Registration Form")
    label_0 = Label(root, text="Registration form", width=20, font=headerFont, fg='red')
    label_0.place(x=10, y=53)
    label_1 = Label(root, text="Student ID", width=20, font=myFont)
    label_1.place(x=10, y=130)
    entry_1 = Entry(root, font=myFont)
    entry_1.place(x=200, y=130)
    label_2 = Label(root, text="Name", width=20, font=myFont)
    label_2.place(x=32, y=180)
    entry_2 = Entry(root, font=myFont)
    entry_2.place(x=200, y=180)
    label_3 = Label(root, text="Password", width=20, font=myFont)
    label_3.place(x=18, y=230)
    entry_3 = Entry(root, show='*', font=myFont)
    entry_3.place(x=200, y=230)
    label_4 = Label(root, text="Vjudge Handle", width=20, font=myFont)
    label_4.place(x=-4, y=280)
    entry_4 = Entry(root, font=myFont)
    entry_4.place(x=200, y=280)
    label_5 = Label(root, text="Codeforces Handle", width=20, font=myFont)
    label_5.place(x=-20, y=330)
    entry_5 = Entry(root, font=myFont)
    entry_5.place(x=200, y=330)
    label_6 = Label(root, text="Toph Handle", width=20, font=myFont)
    label_6.place(x=2, y=380)
    entry_6 = Entry(root, font=myFont)
    entry_6.place(x=200, y=380)

    Button(root, text='Submit', width=10, bg='#c6c6c6', fg='red', font=myFont,
           command=lambda: doRegistration(root, entry_1.get(), entry_2.get(), entry_3.get(), entry_4.get(),
                                          entry_5.get(), entry_6.get())).place(x=100, y=450)
    Button(root, text='Go Back', width=10, bg='black', fg='white', font=myFont,
           command=lambda: startpage(root)).place(x=260,y=450)

    root.mainloop()


def loginpage(root):
    root.destroy()
    root = Tk()
    root.geometry('500x500')
    myFont = fonts.Font(family='Georgia', size=18)
    headerFont = fonts.Font(family='Century Schoolbook', size=30)
    insertFont = fonts.Font(family='Century Schoolbook', size=12)
    root.resizable(FALSE, FALSE)
    root.title("Login Form")
    label_0 = Label(root, text="Login form", width=20, fg='Red', font=headerFont)
    label_0.place(x=20, y=53)
    label_1 = Label(root, text="User ID:", width=20, font=myFont)
    label_1.place(x=5, y=150)
    entry_1 = Entry(root,font=myFont, width=15)
    entry_1.place(x=200, y=150)
    label_2 = Label(root, text="Password:", width=20, font=myFont)
    label_2.place(x=-3, y=230)
    entry_2 = Entry(root, show='*', font=myFont, width=15)
    entry_2.place(x=200, y=230)
    Button(root, text='Submit', width=10, bg='#c6c6c6', fg='red', font=myFont,
           command=lambda: login(root, entry_1.get(), entry_2.get())).place(x=100, y=320)
    Button(root, text='Go Back', width=10, bg='black', fg='white', font=myFont,
           command=lambda: startpage(root)).place(x=270, y=320)

    root.mainloop()


def startpage(root):
    root.destroy()
    root = Tk()
    root.title('welcome page')
    root.geometry('500x500')
    root.resizable(FALSE, FALSE)
    frame = Frame(root).place(x=500, y=500)
    myFont = fonts.Font(family='Georgia', size=12)
    headerFont = fonts.Font(family='Century Schoolbook', size=18)
    insertFont = fonts.Font(family='Century Schoolbook', size=10)
    Label(root, text="Welcome to IUTPC Rating System", font=headerFont, fg='#bf2626').place(x=60, y=120)
    Button(root, text='Register', width=15, bg='#bf2626', fg='white', font=myFont, border=5, command=lambda: registration(root))\
        .place(x=100, y=320)
    Button(root, text='Login', width=15, bg='#bf2626', fg='white', font=myFont, border=5, command=lambda: loginpage(root))\
        .place(x=260, y=320)
    root.mainloop()


# init welcome page
if __name__ == "__main__":
    root = Tk()
    startpage(root)

# registrationpage
