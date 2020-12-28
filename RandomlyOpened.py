import requests
import bs4 as bs
from selenium import webdriver
from tkinter import *
import cx_Oracle as Cx
from tkinter.ttk import Treeview



def returnFunction(tup):
    (root, ret) = tup
    root.destroy()
    print(ret)


def vjudgeverify(url):
    # root.mainloop()
    driver = webdriver.Chrome("D:\\Setup Files\\chromedriver_win32\\chromedriver.exe")
    driver.get(url)
    res = driver.execute_script("return document.documentElement.outerHTML;")
    soup = bs.BeautifulSoup(res, 'lxml')
    driver.quit()
    contest_table = soup.find('table', id='contest-rank-table')
    cnt = 0;
    li = []
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
                handle = x.split()[0]
            elif cnt == 2:
                solved = int(x)
            elif cnt == 3:
                time_penalty = int(x.split()[0])
            cnt = cnt + 1
        dict = {'handle': handle, 'solved': solved, 'time_pen': time_penalty}
        if dict['handle'] != '':
            li.append(dict)
    return li


def AddToRankList(root, listOfSelectedParicipants, solv, tpp, name, url, div, man, plat):
    print(listOfSelectedParicipants)


def getContestStatus(name,url, plat, div, man):
    if plat == 'codeforces':
        print('hudai')
    else:
        li = vjudgeverify(url)
        root = Tk()
        root.geometry('1200x790')
        Label(root, text='Temporary Point Table', fg='red').place(x=500, y=70)
        conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
        cur = conn.cursor()
        if div == 0:
            cur.execute('select userid,vjudge_handle from handle_info')
        else:
            stmt = 'select userid,vjudge_handle from handle_info where division_id = ' + div
            print(stmt)
            cur.execute(stmt)

        rs = cur.fetchall()
        listOfSelectedParicipants = []
        dic = {}
        for item in rs:
            dic[item[1]] = item[0]
            listOfSelectedParicipants.append(item[1])
        for item in listOfSelectedParicipants:
            print(item)
        print('hello world!')
        solv = {}
        tpp = {}
        for item in li:
            solv[item['handle']] = item['solved']
            tpp[item['handle']] = item['time_pen']
        tv = Treeview(root, columns=(1, 2, 3, 4,5), show="headings", height='20')
        tv.heading(1, text='Position')
        tv.heading(2, text='Student ID')
        tv.heading(3, text='Handle')
        tv.heading(4, text='Solved')
        tv.heading(5, text='Time Penalty')
        poos = 1
        for item in listOfSelectedParicipants:
            hand = item
            sid = dic[item]
            try:
                sv = solv[item]
            except KeyError:
                sv = 0
            try:
                timep = tpp[item]
            except KeyError:
                timep = 0

            tv.insert("", "end", values=(poos, sid, hand, sv, timep))
            poos=poos+1
        tv.place(x=150, y=180)
        Button(root, text='Create Ranking and Save', fg='red', bg='grey',command= lambda :AddToRankList(root,listOfSelectedParicipants,solv,tpp,name,url,div,man,plat)).place(x=270, y=740)
        root.mainloop()
    return


if __name__ == '__main__':
    getContestStatus('ncpc selection contest','https://vjudge.net/contest/354497#rank', 'vjudge', 0, 0)
