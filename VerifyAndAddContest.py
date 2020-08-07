import requests
import bs4 as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tkinter import *
import cx_Oracle as Cx
from tkinter.ttk import Treeview
import math
import adminhomepage
import CFStandingFetcher
from TophStandingFetcher import *


def returnFunction(tup):
    (root, ret) = tup
    root.destroy()
    print(ret)


def vjudgeverify(url):
    print(url)
    # root.mainloop()
    driver = webdriver.Firefox(executable_path="D:\\Setup Files\\chromedriver_win32\\geckodriver.exe")
    driver.get(url + '#rank')
    res = driver.execute_script("return document.documentElement.outerHTML;")
    soup = bs.BeautifulSoup(res, 'lxml')
    driver.quit()
    contest_table = soup.find('table', id='contest-rank-table')
    cnt = 0
    li = {}
    for row in contest_table.find_all('tr'):
        handle = ''
        solved = 0
        time_penalty = 0
        cnt = 0
        for cell in row.find_all('td'):
            x = cell.text
            x = x.lstrip()
            x = x.rstrip()
            if cnt == 1:
                try:
                    handle = x.split()[0]
                    handle = handle.lower()
                    print(handle)
                except:
                    continue

            elif cnt == 2:
                solved = int(x)
            elif cnt == 3:
                time_penalty = int(x.split()[0])
            cnt = cnt + 1
        dict = {'solved': solved, 'time_pen': time_penalty}
        if handle != '':
            li[handle] = dict
    return li


def generateSeed(root, totalRanklist, item, rating):
    sum = 0
    for others in totalRanklist:
        if others[2] == item[2]:
            continue
        else:
            prob = 1 + pow(10, (-others[3] + rating) / 400)
            sum = sum + (1 / prob)
    sum += 1
    return sum


def generateWinProbability(a, b):
    return 1.0 / (1 + pow(10, (b - a) / 400.0))


def showContestRanklist(root):
    return


def addToDatabase(root, finalRankList, name, url, plat, div, man, handleToStudentID):
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    insertContest = 'insert into contest_info(contest_name,contest_url,platform_id,division,mandatory) values( \'' + name + '\',\'' + url + '\',\'' + plat + '\', ' + str(
        div) + ' , ' + str(man) + ')'
    try:
        cur.execute(insertContest)
    except Cx.IntegrityError:
        print('error')
    selectcid = 'select max(contest_id) from contest_info where contest_name = \'' + name + '\' and contest_url = \'' + url + '\''
    cur.execute(selectcid)
    rs = cur.fetchall()
    print(rs[0][0])
    cid = rs[0][0]
    for item in finalRankList:
        handle = item[0]
        position = item[1]
        solved = item[2]
        time_pen = item[3]
        rating = item[4]
        print(handle)
        sid = handleToStudentID[handle]
        insertRanklist = 'insert into ranklist values(\'' + cid + '\',\'' + sid + '\', ' + str(solved) + ' , ' + str(
            time_pen) + ',' + str(item[5]) + ')'
        cur.execute(insertRanklist)
        updateRating = 'update current_rating set overall_rating = ' + str(rating) + ' where userid = \'' + sid + '\''
        print(updateRating)
        cur.execute(updateRating)
    print('done')
    for item in finalRankList:
        handle = item[0]
        position = item[1]
        solved = item[2]
        time_pen = item[3]
        rating = item[4]
        print(handle)
        sid = handleToStudentID[handle]
        updateRating = 'update current_rating set overall_rating = ' + str(rating) + ' where userid = \'' + sid + '\''
        print(updateRating)
        cur.execute(updateRating)
    conn.commit()
    print('done')
    adminhomepage.adminWelcomePage(root)


def AddToRankList(root, totalRanklist, name, url, plat, div, man, handleToStudentID):
    seed = []
    totalRanklist.sort(key=lambda x: (x[0], -x[1], -x[3]), reverse=True)
    pos = 1
    print(totalRanklist)
    newRanklist = []
    changeRating = []
    for item in totalRanklist:
        if pos == pos:
            sid = generateSeed(root, totalRanklist, item, item[3])
            m = (sid * pos) ** (0.5)
            # print(sid, pos, m)
            hi = 8000
            lo = 1
            while hi - lo > 1:
                mid = (hi + lo) / 2
                if generateSeed(root, totalRanklist, item, mid) < m:
                    hi = mid
                else:
                    lo = mid
            # print(lo)
            change = (lo - item[3]) / 2
            if item[0] == 0 and item[1] == 0:
                newRanklist.append(int(item[3] - abs(change)))
                changeRating.append(int(-abs(change)))
            else:
                newRanklist.append(int(item[3] + change))
                changeRating.append(int(change))
        pos += 1
    print(newRanklist)
    new_item = []
    for i in range(0, len(totalRanklist)):
        new_item.append(
            (totalRanklist[i][2], i + 1, totalRanklist[i][0], totalRanklist[i][1], newRanklist[i], changeRating[i]))

    for item in new_item:
        print(item)
    addToDatabase(root, new_item, name, url, plat, div, man, handleToStudentID)


def getrating(sid):
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    cur.execute("select overall_rating from current_rating where userid = \'" + sid + '\'')
    rs = cur.fetchall()
    return rs[0][0]


def getStudentId(handle, platform):
    print(handle)
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    if platform == 'vjudge':
        cur.execute('select userid from handle_info where VJUDGE_HANDLE = \'' + handle + '\'')
        rs = cur.fetchall()
        if len(rs) == 0:
            print('not found')
            return '170041014'
        else:
            return rs[0][0]
    else:
        cur.execute('select userid from handle_info where cf_handle = \'' + handle + '\'')
        rs = cur.fetchall()
        return rs[0][0]


def generateSeedCF(root, totalRanklist, item, rating):
    sum = 0
    for others in totalRanklist:
        if others[2] == item[2]:
            continue
        else:
            prob = 1 + pow(10, (-others[4] + rating) / 400)
            sum = sum + (1 / prob)
    sum += 1
    return sum


def addToDatabaseCF(root, finalRankList, changeRating, li, name, url, div, man):
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    insertContest = 'insert into contest_info(contest_name,contest_url,platform_id,division,mandatory) values( \'' + name + '\',\'' + url + '\',\'' + 'codeforces' + '\', ' + str(
        div) + ' , ' + str(man) + ')'
    try:
        cur.execute(insertContest)
    except Cx.IntegrityError:
        print('error')
    selectcid = 'select max(contest_id) from contest_info where contest_name = \'' + name + '\' and contest_url = \'' + url + '\''
    cur.execute(selectcid)
    rs = cur.fetchall()
    print(rs[0][0])
    cid = rs[0][0]
    poos = 1
    for item in li:
        handle = item[0]
        position = poos
        solved = item[2]
        time_pen = item[3]
        rating = item[4] + changeRating[poos - 1]
        print(handle)
        insertRanklist = 'insert into ranklist values(\'' + cid + '\',\'' + handle + '\', ' + str(solved) + ' , ' + str(
            time_pen) + ',' + str(changeRating[poos - 1]) + ')'
        cur.execute(insertRanklist)
        conn.commit()
        updateRating = 'update current_rating set overall_rating = ' + str(
            rating) + ' where userid = \'' + handle + '\''
        print(updateRating)
        cur.execute(updateRating)
        poos += 1
        conn.commit()
    print('done')
    conn.commit()
    print('done')
    adminhomepage.adminWelcomePage(root)


def addToRanklistForCF(root, li, name, url, div, man):
    seed = []
    pos = 1
    print(li)
    newRanklist = []
    changeRating = []
    for item in li:
        if pos == pos:
            sid = generateSeedCF(root, li, item, item[4])
            m = (sid * pos) ** (0.5)
            # print(sid, pos, m)
            hi = 8000
            lo = 1
            while hi - lo > 1:
                mid = (hi + lo) / 2
                if generateSeedCF(root, li, item, mid) < m:
                    hi = mid
                else:
                    lo = mid
            # print(lo)
            change = (lo - item[4]) / 2
            if item[0] == 0 and item[1] == 0:
                newRanklist.append(int(item[4] - abs(change)))
                changeRating.append(int(-abs(change)))
            else:
                newRanklist.append(int(item[4] + change))
                changeRating.append(int(change))
        pos += 1
    print(newRanklist)
    addToDatabaseCF(root, newRanklist, changeRating, li, name, url, div, man)
    return

def generateSeedTOPH(root, position, rating, currentrating):
    sum = 0
    for others in range(0,len(rating)):
        if others == position:
            continue
        else:
            prob = 1 + pow(10, (-rating[others] + currentrating) / 400)
            sum = sum + (1 / prob)
    sum += 1
    return sum

def addToDatabaseTOPH(root, li,rating, changeRating, name, url, div, man):
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    statement = 'insert into contest_info(contest_name,contest_url,platform_id,division,mandatory) values( \'' + name + '\',\'' + url + '\',\'' + 'toph' + '\', ' + str(
        div) + ' , ' + str(man) + ')'
    print(statement)
    cur.execute(statement)
    try:
        cur.execute(statement)
    except Cx.IntegrityError:
        print('error')
    selectcid = 'select max(contest_id) from contest_info where contest_name = \'' + name + '\' and contest_url = \'' + url + '\''
    cur.execute(selectcid)
    rs = cur.fetchall()
    print(rs[0][0])
    cid = rs[0][0]

    poos = 1
    for item in li:
        handle = item[1]
        position = item[0]
        solved = item[2]
        time_pen = item[3]
        insertRanklist = 'insert into ranklist values(\'' + cid + '\',\'' + handle + '\', ' + str(solved) + ' , ' + str(
            time_pen) + ',' + str(changeRating[poos - 1]) + ')'
        cur.execute(insertRanklist)
        conn.commit()
        updateRating = 'update current_rating set overall_rating = ' + str(int(rating[poos-1]+changeRating[poos-1])) + ' where userid = \'' + handle + '\''
        print(updateRating)
        cur.execute(updateRating)
        poos += 1
        conn.commit()
    adminhomepage.adminWelcomePage(root)


def addToRanklistForTOPH(root,li,name,url,div,man):
    rating = []
    for items in li:
        conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
        cur = conn.cursor()
        statement = 'select overall_rating  from current_rating  where userid = \'' + items[1] + '\''
        print(items[1])
        cur.execute(statement)
        rs = cur.fetchall()
        rating.append(rs[0][0])
        conn.close()
    changeRating = []
    pos = 1
    for item in range(0,len(li)):
        sid = generateSeedTOPH(root, pos, rating, rating[item])
        m = (sid * pos) ** (0.5)
        hi = 8000
        lo = 1
        while hi - lo > 1:
            mid = (hi + lo) / 2
            if generateSeedTOPH(root, pos, rating, mid) < m:
                hi = mid
            else:
                lo = mid
        change = (lo - rating[item]) / 2
        pos += 1
        changeRating.append(int(change))
    addToDatabaseTOPH(root, li,rating, changeRating, name, url, div, man)
    return


def processStandingToph(li):
    processedStanding = []
    #li =  han, stid, solved, tp
    position = 1
    print(li)
    for item in li:
        conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
        cur = conn.cursor()
        statement = 'select overall_rating  from current_rating  where userid = \'' + item[0] + '\''
        cur.execute(statement)
        rs = cur.fetchall()
        print(rs[0][0])
        processedStanding.append((item[1], item[0], item[2], item[3], rs[0][0]))
        conn.close()
    processedStanding.sort(key=lambda x: (x[2], -x[3], -x[4]), reverse=True)
    finalList = []
    for items in processedStanding:
        print(items)
        finalList.append((position,items[0],items[2],items[3],items[4]))
        position += 1
    print(finalList)
    return processedStanding




def getContestStatus(url, name, plat, div, man):
    if plat == 'toph':
        li = getStandingToph(name,url,div,man)
        if(type(li)!=list):
            print("NOT REACHABLE")
        else:
            li = processStandingToph(li)
            root = Tk()
            root.geometry('1200x790')
            Label(root, text='Temporary Point Table', fg='red').place(x=500, y=70)
            tv = Treeview(root, columns=(1, 2, 3, 4, 5), show="headings", height='20')
            tv.heading(1, text='Position')
            tv.heading(2, text='Student ID')
            tv.heading(3, text='Handle')
            tv.heading(4, text='Solved')
            tv.heading(5, text='Time Penalty')
            poos = 1
            for item in li:
                tv.insert("", "end", values=(poos, item[0], item[1], item[2], item[3]))
                poos = poos + 1
            tv.place(x=150, y=180)
            Button(root, text='Create Ranking and Save', fg='red', bg='grey',
                   command=lambda: addToRanklistForTOPH(root, li, name, url, div, man)).place(x=270, y=740)
            root.mainloop()
        #li is a dictionary that returns handle, sid, solved, timepenalty
    elif plat == 'codeforces':
        li = CFStandingFetcher.getStanding(url, name, div, man)
        print(li)
        root = Tk()
        root.geometry('1200x790')
        Label(root, text='Temporary Point Table', fg='red').place(x=500, y=70)
        tv = Treeview(root, columns=(1, 2, 3, 4, 5), show="headings", height='20')
        tv.heading(1, text='Position')
        tv.heading(2, text='Student ID')
        tv.heading(3, text='Handle')
        tv.heading(4, text='Solved')
        tv.heading(5, text='Time Penalty')
        poos = 1
        for item in li:
            tv.insert("", "end", values=(poos, item[0], item[1], item[2], item[3]))
            poos = poos + 1
        tv.place(x=150, y=180)
        Button(root, text='Create Ranking and Save', fg='red', bg='grey',
               command=lambda: addToRanklistForCF(root, li, name, url, div, man)).place(x=270, y=740)
        root.mainloop()

    else:
        li = vjudgeverify(url)
        print(li)
        root = Tk()
        root.geometry('1200x790')
        Label(root, text='Temporary Point Table', fg='red').place(x=500, y=70)
        conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
        cur = conn.cursor()

        if div == 0:
            cur.execute('select userid,vjudge_handle from handle_info')
        else:
            stmt = 'select userid,vjudge_handle from handle_info where division_id = ' + str(div)
            print(stmt)
            cur.execute(stmt)

        rs = cur.fetchall()
        listOfSelectedParicipants = []
        handleToStudentID = {}
        for item in rs:
            handleToStudentID[item[1]] = item[0]
            listOfSelectedParicipants.append(item[1])
        for item in listOfSelectedParicipants:
            print(item)
        print('hello world!')
        solv = {}
        tpp = {}
        lii = []
        for item in listOfSelectedParicipants:
            try:
                xx = li[item]['solved']
            except KeyError:
                if man == 0:
                    lii.append((0, 0, item, getrating(handleToStudentID[item])))
            else:
                lii.append((li[item]['solved'], li[item]['time_pen'], item, getrating(handleToStudentID[item])))

        lii.sort(key=lambda x: (x[0], -1 * x[1]), reverse=True)
        print(lii)
        # for item in lii:
        #     solv[item[2]] = item]['solved']
        #     tpp[item] = li[item]['time_pen']
        tv = Treeview(root, columns=(1, 2, 3, 4, 5), show="headings", height='20')
        tv.heading(1, text='Position')
        tv.heading(2, text='Student ID')
        tv.heading(3, text='Handle')
        tv.heading(4, text='Solved')
        tv.heading(5, text='Time Penalty')
        poos = 1
        for item in lii:
            tv.insert("", "end", values=(poos, handleToStudentID[item[2]], item[2], item[0], item[1]))
            poos = poos + 1
        tv.place(x=150, y=180)
        Button(root, text='Create Ranking and Save', fg='red', bg='grey',
               command=lambda: AddToRankList(root, lii, name, url, plat, div, man, handleToStudentID)).place(x=270,
                                                                                                             y=740)
        root.mainloop()
    return


if __name__ == '__main__':
    getContestStatus('Toph1', 'criterion-2020-round-3', 'toph', 0, 0)
