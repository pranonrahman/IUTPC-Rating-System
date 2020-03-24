import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from tkinter import *


def returnFunction(tup):
    (root, ret) = tup
    print(ret)

def vjudgeverify(url):
    root = Tk()
    root.geometry('200x200')
    Label(root, text='Loading Contest in vjudge\n Please Wait until the box closes').place(x=40,y=40)
    driver = webdriver.Chrome("D:\\Setup Files\\chromedriver_win32\\chromedriver.exe")
    driver.get(url)
    res = driver.execute_script("return document.documentElement.outerHTML;")
    soup = BeautifulSoup(res, 'xml')
    print(soup.text)
    return (root, 1)
    root.mainloop()
    driver.quit()


def getContestStatus(url, plat):
    if plat=='codeforces':
        print('hudai')
    else:
        vjudgeverify(url)
    return