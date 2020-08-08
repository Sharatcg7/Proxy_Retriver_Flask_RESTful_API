import datetime

import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import urllib.request
import socket
import urllib.error
import time
import json


e = create_engine('sqlite:///database.db')

#function to retrive proxy lists
def get_proxy_list(url):
    proxieslist = []
    if 'rapidapi' in url:

        querystring = {"limit": "150", "type": "HTTPS"}

        headers = {
            'x-rapidapi-host': "proxypage1.p.rapidapi.com",
            'x-rapidapi-key': "6c57d35416msh577a78de53cc96ap18190ajsnaaa53be816e6",
            'content-type': "application/x-www-form-urlencoded"
        }

        response = requests.get(url, headers=headers, params=querystring)
        json_data = json.loads(response.text)
        for data in json_data:
            dict_line = {'IP': str(data['ip']), 'Port': str(data['port'])}
            proxieslist.append(dict_line)

    else:
        r = requests.get(url)
        proxy_response = BeautifulSoup(r.content, 'lxml')
        table = proxy_response.find('table')
        rows = table.find_all('tr')
        for row in rows:
            ip = row.contents[0].text
            port = row.contents[1].text
            secureconn = row.contents[6].text

            if (secureconn == 'yes'):
                dict_line = {'IP': ip, 'Port': port}
                proxieslist.append(dict_line)

    return proxieslist

def is_bad_proxy(pip, testurl):
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': pip})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        req = urllib.request.Request(testurl)
        sock = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print('Error code: ', e.code)
        return e.code
    except Exception as detail:
        print("ERROR:", detail)
        return True
    return False


def basicproxytest(proxies, date):
    conn = e.connect()
    for proxy in proxies:
        line = 'https://'+ proxy['IP'] + ':' + proxy['Port']
        proxies = {'http': line, 'https': line}
        print(proxies)
        try:
            testIP = requests.get('https://httpbin.org/ip', proxies = proxies, timeout = 0.5)
            resposeIP = testIP.json()['origin']
            origin = resposeIP.split(',')
            if (origin[0] == proxy['IP']):
                print(proxy['IP'])
                conn.execute("UPDATE proxylists SET basictest = ? WHERE IP = ?",
                             (date, proxy['IP']))
        except:
            print('Bad Proxies')

    if (conn):
        conn.close()
        print("The SQLite connection is closed")

def proxiestodb(proxies, date):
    conn = e.connect()
    for proxy in proxies:
        try:
            conn.execute("insert into proxylists (IP, Port, insertdate, lastupdate) values (?, ?, ?, ?)",
                                 (proxy['IP'], proxy['Port'], date, date))
            print('Data has been stored successfully')
        except:
            conn.execute("UPDATE proxylists SET lastupdate = ? WHERE IP = ?",
                                 (date, proxy['IP']))
            print('Lastupdate has been stored sucessfully')

    if (conn):
        conn.close()
        print("The SQLite connection is closed")

def updateprovidertable(url, date, records):
    records = len(records)
    conn = e.connect()
    try:
        conn.execute("UPDATE proxyprovider SET  lastupdate = ?, recordsfound = ? WHERE baseurl = ?",
                     (date, records, url))
        msg = 'Data has been updated successfully'
        print(msg)
    except:
        msg = 'Error while updating provider table !'
        print(msg)

    if (conn):
        conn.close()
        print("The SQLite connection is closed")


def functesturl(proxies, url):
    testurl = 'https://'+ url
    conn = e.connect()
    goodproxy = []
    badproxy = []
    date = str(datetime.datetime.now())
    dataformat = date[0:10] + ',' + date[11:19]

    socket.setdefaulttimeout(120)
    for currentproxy in proxies:
        proxy_IP = currentproxy.split(':')

        if is_bad_proxy(currentproxy, testurl):
            print('not working. . . .')
            badproxy.append(currentproxy)
        else:
            print('working . . .')
            conn.execute("UPDATE proxylists SET urltest = ? WHERE IP = ?",
                         (dataformat, proxy_IP[0]))
            goodproxy.append(currentproxy)

    recordsfound = len(goodproxy)
    try:
        conn.execute("insert into proxytest (testurl, successrecords, testdate) values (?, ?, ?)",
                     (testurl, recordsfound, dataformat ))
    except:
        conn.execute("UPDATE proxytest SET successrecords = ?, testdate = ? WHERE testurl = ?",
                     (recordsfound, dataformat, testurl))

    if (conn):
        conn.close()
        print('completed . . ')
        print("The SQLite connection is closed")


def updatedb(jsondata):
    proxylist = []
    date = str(datetime.datetime.now())
    dataformat = date[0:10] + ',' + date[11:19]
    proxylist.append(jsondata)

    proxiestodb(proxylist, dataformat)
    print('Proxies --> Database completed ')

    basicproxytest(proxylist, dataformat)
    print('proxies --> basicproxytest completed')

def backendserverupdate():

    urls = ["https://www.sslproxies.org/", "https://free-proxy-list.net/", "https://proxypage1.p.rapidapi.com/v1/tier1"]

    for url in urls:
        print(url)

        proxies = get_proxy_list(url)
        print(proxies)

        date = str(datetime.datetime.now())
        dataformat = date[0:10] + ',' + date[11:19]

        updateprovidertable(url, dataformat, proxies)

        proxiestodb(proxies, dataformat)
        print('Proxies --> Database completed ')

        basicproxytest(proxies, dataformat)
        print('proxies --> basicproxytest completed')

if __name__ == '__main__':
    while True:
        backendserverupdate()
        time.sleep(600)
        print('Updating the server...')


