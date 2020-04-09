from tkinter import *
import cx_Oracle as Cx
from welcomepage import *
import welcomepage


#
# def showStudentInfo(root,sid):
#     root.destroy()
#     root = Tk()
#     root.title('pending request')
#     root.geometry('1200x750')
#     root.resizable(FALSE, FALSE)
#     return


def ShowOtherStudents(root, sid):
    root.destroy()
    root = Tk()
    root.title('Student List')
    root.geometry('1200x750')
    root.resizable(FALSE, FALSE)
    Label(root, text='Student List', fg='red', font=('bold', 28)).place(x=490, y=70)
    b2 = Button(root, text='Go Back', fg='red', width=20, command=lambda: studentWelcomePage(root, sid))
    b2.place(x=520, y=140)
    tv = Treeview(root, columns=(1, 2, 3, 4, 5), show="headings", height='20')
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
    tv.place(x=100, y=180)
    return


def showRatingChanges(root,sid):
    root.destroy()
    root = Tk()
    root.title('Student List')
    root.geometry('1200x750')
    root.resizable(FALSE, FALSE)
    Label(root, text='Student List', fg='red', font=('bold', 28)).place(x=490, y=70)
    b2 = Button(root, text='Go Back', fg='red', width=20, command=lambda: studentWelcomePage(root, sid))
    b2.place(x=520, y=140)
    tv = Treeview(root, columns=(1, 2, 3, 4), show="headings", height='20')
    tv.heading(1, text='Contest ID')
    tv.heading(2, text='Name')
    tv.heading(3, text='Platform')
    tv.heading(4, text='Rating Change')
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    stmt = 'select contest_info.contest_id,contest_info.contest_name,contest_info.platform_id,ranklist.change_rating from contest_info,ranklist where contest_info.contest_id = ranklist.contest_id and ranklist.userid = \'' + sid + '\''
    cur.execute(stmt)
    rs = cur.fetchall()
    for row in rs:
        SID = row[0]
        un = row[1]
        vj = row[2]
        cf = row[3]
        tv.insert("", "end", values=(SID, un, vj, cf))
    tv.place(x=100, y=180)
    return


def studentWelcomePage(root, sId):
    root.destroy()
    root = Tk()
    root.geometry('1250x400')
    root.resizable(FALSE, FALSE)
    rating = 0
    sid = sId
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    stmt = 'select overall_rating from current_rating where userid=\'' + sid + "\'"
    cur.execute(stmt)
    rs = cur.fetchall()
    rating = rs[0][0]
    Label(root, text='Welcome to IUTPC Rating System(Student Module)', fg='red', font=('bold', 20)).place(x=300, y=50)
    if 0 < rating < 1200:
        Label(root, text='Student ID: ' + sid, fg='grey', font=(14)).place(x=400, y=120)
        Label(root, text='Rating: ' + str(rating), fg='grey', font=(14)).place(x=650, y=120)
    if 1200 < rating < 1601:
        Label(root, text='Student ID: ' + sid, fg='green', font=(14)).place(x=400, y=120)
        Label(root, text='Rating: ' + str(rating), fg='green', font=(14)).place(x=650, y=120)
    if 1600 < rating < 2001:
        Label(root, text='Student ID: ' + sid, fg='blue', font=(14)).place(x=400, y=120)
        Label(root, text='Rating: ' + str(rating), fg='blue', font=(14)).place(x=650, y=120)
    if 2000 < rating < 2401:
        Label(root, text='Student ID: ' + sid, fg='purple', font=(14)).place(x=400, y=120)
        Label(root, text='Rating: ' + str(rating), fg='purple', font=(14)).place(x=650, y=120)
    if 2400 < rating < 2801:
        Label(root, text='Student ID: ' + sid, fg='orange', font=(14)).place(x=400, y=120)
        Label(root, text='Rating: ' + str(rating), fg='orange', font=(14)).place(x=650, y=120)
    if 2800 < rating:
        Label(root, text='Student ID: ' + sid, fg='red', font=(14)).place(x=400, y=120)
        Label(root, text='Rating: ' + str(rating), fg='red', font=(14)).place(x=650, y=120)

    Button(root, text='Other Students Rating', width=20, height=5, fg='red', borderwidth=3,
           command=lambda: ShowOtherStudents(root, sid)).place(x=340, y=200)
    Button(root, text='Rating Changes', width=20, height=5, fg='red', borderwidth=3, command = lambda :showRatingChanges(root,sid)).place(x=510, y=200)
    Button(root, text='Logout', width=20, height=5, bg='grey', fg='red', borderwidth=3,
           command=lambda: welcomepage.startpage(root)).place(x=675, y=200)
    root.mainloop()


if __name__ == '__main__':
    root = Tk()
    studentWelcomePage(root, '170041014')
    root.mainloop()
