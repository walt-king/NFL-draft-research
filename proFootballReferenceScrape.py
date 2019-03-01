# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 19:01:53 2019

@author: Walter King
"""

## Big credit to @BenKite for this one, I adapted their code to fit my needs
## Original Source: https://github.com/BenKite/football_data/blob/master/profootballReferenceScrape.py

import pandas
import requests, bs4
from bs4 import BeautifulSoup
import re
import urllib

def findTables(url):
    res = requests.get(url)
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
    divs = soup.findAll('div', id = "content")
    divs = divs[0].findAll("div", id=re.compile("^all"))
    ids = []
    for div in divs:
        searchme = str(div.findAll("table"))
        x = searchme[searchme.find("id=") + 3: searchme.find(">")]
        x = x.replace("\"", "")
        if len(x) > 0:
            ids.append(x)
    return(ids)

def pullTable(url, tableID, header = False):
    res = requests.get(url)
    ## Work around comments
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
    tables = soup.findAll('table', id = tableID)
    data_rows = tables[0].findAll('tr')
    game_data = [[td.getText() for td in data_rows[i].findAll(['th','td'])]
        for i in range(len(data_rows))
        ]
    data = pandas.DataFrame(game_data)
    if header == True:
        data_header = tables[0].findAll('thead')
        data_header = data_header[0].findAll("tr")
        data_header = data_header[0].findAll("th")
        header = []
        for i in range(len(data.columns)):
            header.append(data_header[i].getText())
        data.columns = header
        data = data.loc[data[header[0]] != header[0]]
    data = data.reset_index(drop = True)
    return(data)
 
def pullLinks(url, tableID, header = False):
    res = requests.get(url)
    ## Work around comments
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
    tables = soup.findAll('table', id = tableID)
    data_rows = tables[0].findAll('tr')
    game_data = [[td.get('href') for td in data_rows[i].findAll(['a'])]
        for i in range(len(data_rows))
        ]
    data = pandas.DataFrame(game_data)
    if header == True:
        data_header = tables[0].findAll('thead')
        data_header = data_header[0].findAll("tr")
        data_header = data_header[0].findAll("th")
        header = []
        for i in range(len(data.columns)):
            header.append(data_header[i].getText())
        data.columns = header
        data = data.loc[data[header[0]] != header[0]]
    data = data.reset_index(drop = True)
    return(data)



year = 2007
    
url = "https://www.pro-football-reference.com/years/" + str(year) + "/draft.htm"

table_data = pullTable(url, "drafts")
table_links = pullLinks(url, "drafts")

## Pull player name, Pro-Football-Reference and CFB-Reference page url
player_list = table_data[3].values.tolist()
cfb_ref_list = table_links[3].values.tolist()
nfl_ref_list = table_links[1].values.tolist()

for i in range(0, len(player_list)):
    player_list[i] = [player_list[i]]
    if nfl_ref_list[i] == None:
        player_list[i].append('')
    else:
        player_list[i].append("https://www.pro-football-reference.com" + str(nfl_ref_list[i]))
    if cfb_ref_list[i] == None:
        player_list[i].append('')
    else:
        player_list[i].append(cfb_ref_list[i])

## Pull birth date from Pro-Football-Reference
## It's not perfect, but it pulls the html snippet containing birth date
## 18:28 extracts birth date as a yyyy-mm-dd date string
for i in range(0, len(player_list)):
    url = player_list[i][1]
    try:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
    except:
        print("Invalid URL")
    try:
        font = soup.find_all('span', {"itemprop":"birthDate", "id":"necro-birth"})[0]
        player_list[i].append(str(font)[18:28])
    except:
        player_list[i].append('')


dumpfile = open('dumpfile.csv','w')
for index in range(len(player_list)):
    try:
        writeLine = player_list[index][0] + ',' \
        + player_list[index][1] + ',' \
        + player_list[index][2] + ',' \
        + player_list[index][3] + '\n'
        dumpfile.write(writeLine)
    except:
        writeLine = player_list[index][0]
        dumpfile.write(writeLine)
dumpfile.close()



