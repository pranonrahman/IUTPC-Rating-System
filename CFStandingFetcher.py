import requests
import json
import cx_Oracle as Cx


def fetchStanding(url, li, man):
    cid = url.split('/')[-1]
    print(cid)
    rat = {}
    for row in li:
        print(row[0],row[1])
        rat[row[0]]=row[1]
    print(rat)
    url = 'https://codeforces.com/api/contest.standings?contestId=' + str(cid) + '&showUnfficial=false&handles='
    print(url)
    for handle in li:
        url = url + ';' + handle[0]
    print(url)
    response = requests.get(url)
    response = json.loads(response.text)
    print(type(response))
    response = response['result']['rows']
    #print(response)
    participated = {}
    createStandList=[]
    for row in response:
        #print(row['party']['members'][0]['handle'], row['points'])
        #print(row['party']['members'][0]['handle'],row['points'],0,rat[(row['party']['members'][0]['handle'])])
        try:
            createStandList.append((row['party']['members'][0]['handle'], row['points'],0, rat[row['party']['members'][0]['handle']]))
            participated[(row['party']['members'][0]['handle']).lower()] = 1
        except KeyError:
            continue
    if man == 0:
        for row in li:
            try:
                x = participated[row[0]]
            except KeyError:
                createStandList.append((row[0], 0, 0, row[1]))
    createStandList.sort(key=lambda x: (x[1],-1*x[2],-1*x[3]), reverse=True)
    #print(createStandList)
    return createStandList


def getStanding(url, name, div, man):
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    if div == 0:
        query = 'select userid,cf_handle from handle_info'
    else:
        query = 'select userid,cf_handle from handle_info where division_id = ' + str(div)
    cur = conn.cursor()
    cur.execute(query)
    rs = cur.fetchall()
    cur.execute('select userid,overall_rating from current_rating')
    rs2 = cur.fetchall()
    rat = {}
    for row in rs2:
        rat[row[0]] = row[1]
    handle_sid = {}
    list_handle = []
    for row in rs:
        handle_sid[row[1]] = row[0]
        rating = rat[row[0]]
        list_handle.append((row[1],rating))
    print(list_handle)
    li = fetchStanding(url, list_handle, man)
    final_standing = []
    for row in li:
        han = row[0]
        final_standing.append((handle_sid[han],row[0],row[1],row[2],row[3]))
    print(final_standing)
    return final_standing


if __name__ == '__main__':
    getStanding('https://codeforces.com/contest/1391','Codeforces Round# 632', 0, 0)
