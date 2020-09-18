import requests
from bs4 import BeautifulSoup
import cx_Oracle as Cx
import math


def getStandingToph(contestName,name, div, man):
    handlesAndStudentID = getHandles(div)
    handles = []
    sid = []
    for names in handlesAndStudentID:
        sid.append(names[0])
        handles.append(names[1])
    print(sid)
    print(handles)
    url = 'https://toph.co/c/' + contestName + '/standings'
    response = requests.get(url)
    standings = {}
    if response.status_code != 200:
        print('TOPH NOT REACHABLE')
        return -1
    else:
        # 1 -> handle  3 -> solved + pen 4 .. koyta solved
        soup = BeautifulSoup(response.text, 'lxml')
        #print(response.text)
        table = soup.find_all('table', attrs={'class': 'table standings'})
        currentHandle = ''
        for rows in table[0].find_all('tr'):
            cur = 0
            cnt = 0
            for cells in rows.find_all('td'):
                #print(cells.text, end=' ')
                if cur == 1:
                    currentHandle = cells.text.lower()
                    standings[currentHandle] = [0, 0]
                elif  cur == 3:
                    standings[currentHandle][0] = cells.text
                if cur >= 4 and cells.text.strip() != '':
                    value = cells.text
                    #print(value)
                    solved = int(value.split()[0])
                    if(solved>0):
                        standings[currentHandle][1] += 1
                cur+=1
            if(currentHandle!=''):
                tp = standings[currentHandle][0]
                length = 0
                if standings[currentHandle][1] != 0:
                    length = (int(float(math.log(standings[currentHandle][1], 10)))+1)
                print(length)
                tp = int(float(tp[int(float(length)):]))
                standings[currentHandle][0] = tp
        final_list = []
        for i in range(0, len(handles)):
            stid = sid[i]
            han = handles[i]
            print(han)
            solved = standings.get(han.lower(),[0,0])[1]
            tp = standings.get(han,[0,0])[0]
            final_list.append((stid, han, solved, tp))
        print(final_list)
        return final_list


def getHandles(div):
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    handles = []
    if(div==0):
        statement = 'select userid,toph_handle from handle_info'
        cur.execute(statement)
        rs = cur.fetchall()
        for row in rs:
            handles.append((row[0],row[1]))
    else:
        statement = 'select userid,toph_handle from handle_info where division_id = ' + str(div)
        cur.execute(statement)
        rs = cur.fetch_all()
        for row in rs:
            handles.append((row[0], row[1].lower()))
    return handles
if __name__ == "__main__":
    if type([1,2,3]) == int:
        print('mama hoya gese')
    ls = getHandles(0)
    getStandingToph('criterion-2020-round-1','test',0,1)
