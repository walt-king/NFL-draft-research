# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 07:33:15 2019

@author: Walter King
"""

import urllib
from bs4 import BeautifulSoup

draft_year = 2009
start_num = 0
link_num = 10
##PLAYER RANKINGS BY PAGE (1-25)
##10,13,16,19,22...79,82

url_list = []

while len(url_list) < 300:
    url = "http://www.draftscout.com/members/ratings/top750.php?draftyear=" + \
        str(draft_year) + "&sortby=rateall&order=ASC&startspot=" + str(start_num)
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    link_num = 10
    for i in range(0,25): 
        try:
            link_test = soup.find_all('a', href = True, target = "_blank")[link_num]
            url_add = "http://www.draftscout.com/members/ratings/" + link_test['href']
            url_list.append(url_add)
        except:
            link_num += 0
        link_num += 3
    start_num += 25


player_bio = [0,1,5,7]
##0 = Player Name
##1 = School
##5 = Position
##7 = Class
bio_vals = []

list_vals = []
##NFL COMBINE MEASUREMENTS, assuming Height starts at 4 (it varies), numbers are relative
#4 = Height
#6 = Weight
#8 = 40 Yd
#12 = 20 Yd
#16 = 10 Yd
#20 = Bench Press
#22 = Vertical Jump
#24 = Broad Jump
#26 = 20 Yard Shuttle                    
#28 = 3 Cone Drill
#32 = Hand Size
#34 = Arm Length
#36 = Wingspan

##PRO DAY MEASUREMENTS
#42 = 40 Yd
#44 = 20 Yd
#46 = 10 Yd
#48 = Bench Press
#50 = Vertical Jump
#52 = Broad Jump
#54 = 20 Yard Shuttle
#56 = 3 Cone Drill

player_list = []

for u in range(0, len(url_list)):
    bio_vals = []
    list_vals = []
    ##OPEN PLAYER PAGE
    url = url_list[u]
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    ##PULL PLAYER BIO INFO
    for i in player_bio:
        try:
            font = soup.find_all('font', {"face":"Arial,Helvetica,sans-serif", "size":"-1", "color":"#000000"})[i]
            bio_vals.append(font.text)
        except:
            bio_vals.append('')
    try:
        draft_info = soup.find_all('font', {"face":"Verdana,Geneva,Arial,Helvetica,sans-serif", "size":"-2", "color":"#FFFFFF"})[5]
        drafted = draft_info.text
    except:
        drafted = "Undrafted"
    bio_vals.append(drafted)
    ##PULL MEASUREMENT DATA
    check_num = 0
    check = soup.find_all('font', {"face":"Verdana,Geneva,Arial,Helvetica,sans-serif", "size":"-2", "color":"#000000"})[check_num]
    if check.text != "Height:":                               
        while check.text != "Height:":
            check_num += 1
            check = soup.find_all('font', {"face":"Verdana,Geneva,Arial,Helvetica,sans-serif", "size":"-2", "color":"#000000"})[check_num]
    else:
        check_num = 0
    player_measurements = [check_num + 1, check_num + 3, check_num + 5, check_num + 9, check_num + 13, \
                           check_num + 17, check_num + 19, check_num + 21, check_num + 23, check_num + 25, \
                           check_num + 29, check_num + 31, check_num + 33, check_num + 39, check_num + 41, \
                           check_num + 43, check_num + 45, check_num + 47, check_num + 49, check_num + 51, \
                           check_num + 53]
    for i in player_measurements:
        try:
            font = soup.find_all('font', {"face":"Verdana,Geneva,Arial,Helvetica,sans-serif", "size":"-2", "color":"#000000"})[i]
            list_vals.append(font.text)
        except:
            list_vals.append('')
    ##ORGANIZE DATA INTO DICTIONARY
    player_dict = {"Player Bio":{"Name":bio_vals[0], "School":bio_vals[1], "Position":bio_vals[2], \
             "Class":bio_vals[3], "Drafted":bio_vals[4], "NFL Draft Scout Rank":str(u)}, \
            "NFL Combine":{"Height":list_vals[0], "Weight":list_vals[1], "40 Yd":list_vals[2], "20 Yd":list_vals[3], \
             "10 Yd":list_vals[4], "Bench Press":list_vals[5], "Vertical Jump":list_vals[6], \
             "Broad Jump":list_vals[7], "20 Yard Shuttle":list_vals[8], "3 Cone Drill":list_vals[9], \
             "Hand Size":list_vals[10], "Arm Length":list_vals[11], "Wingspan":list_vals[12]}, \
            "Pro Day":{"40 Yd":list_vals[13], "20 Yd":list_vals[14], "10 Yd":list_vals[15], \
             "Bench Press":list_vals[16], "Vertical Jump":list_vals[17], "Broad Jump":list_vals[18], \
             "20 Yard Shuttle":list_vals[19], "3 Cone Drill":list_vals[20]}}
    ##STORE DATA IN LIST
    player_list.append(player_dict)

print(player_list[0])



dumpfile = open('dumpfile.csv','w')
for index in range(len(player_list)):
    writeLine = player_list[index]["Player Bio"]["Name"] + ',' \
    + player_list[index]["Player Bio"]["School"] + ',' \
    + player_list[index]["Player Bio"]["Position"] + ',' \
    + player_list[index]["Player Bio"]["Class"] + ',' \
    + player_list[index]["Player Bio"]["Drafted"] + ',' \
    + player_list[index]["Player Bio"]["NFL Draft Scout Rank"] + ',' \
    + "NFL Combine" + ',' \
    + player_list[index]["NFL Combine"]["Height"] + ',' \
    + player_list[index]["NFL Combine"]["Weight"] + ',' \
    + player_list[index]["NFL Combine"]["40 Yd"] + ',' \
    + player_list[index]["NFL Combine"]["20 Yd"] + ',' \
    + player_list[index]["NFL Combine"]["10 Yd"] + ',' \
    + player_list[index]["NFL Combine"]["Bench Press"] + ',' \
    + player_list[index]["NFL Combine"]["Vertical Jump"] + ',' \
    + player_list[index]["NFL Combine"]["Broad Jump"] + ',' \
    + player_list[index]["NFL Combine"]["20 Yard Shuttle"] + ',' \
    + player_list[index]["NFL Combine"]["3 Cone Drill"] + ',' \
    + player_list[index]["NFL Combine"]["Hand Size"] + ',' \
    + player_list[index]["NFL Combine"]["Arm Length"] + ',' \
    + player_list[index]["NFL Combine"]["Wingspan"] + ',' \
    + "Pro Day" + ',' \
    + player_list[index]["Pro Day"]["40 Yd"] + ',' \
    + player_list[index]["Pro Day"]["20 Yd"] + ',' \
    + player_list[index]["Pro Day"]["10 Yd"] + ',' \
    + player_list[index]["Pro Day"]["Bench Press"] + ',' \
    + player_list[index]["Pro Day"]["Vertical Jump"] + ',' \
    + player_list[index]["Pro Day"]["Broad Jump"] + ',' \
    + player_list[index]["Pro Day"]["20 Yard Shuttle"] + ',' \
    + player_list[index]["Pro Day"]["3 Cone Drill"] + '\n'
    dumpfile.write(writeLine)
dumpfile.close()









